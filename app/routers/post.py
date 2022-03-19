from fastapi import Response, status, HTTPException, APIRouter, Depends
from random import randrange
from app import oauth2, schemas

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
    ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@router.get("/")
def get_posts(user_id: str = Depends(oauth2.get_current_user)):
    return {"data": my_posts}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, user_id: str = Depends(oauth2.get_current_user)):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return post_dict


@router.get("/{id}")
def get_post(id: int, user_id: str = Depends(oauth2.get_current_user)):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post {id} is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} is not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, user_id: str = Depends(oauth2.get_current_user)):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.Post, user_id: str = Depends(oauth2.get_current_user)):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    
    return post_dict