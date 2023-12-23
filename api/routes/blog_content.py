from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ..schemas import BlogContent, BlogContentResponse, db
from .. import oath2
from datetime import datetime

router = APIRouter(
    prefix="/blog",
    tags=["Blog Content"],
)


# TODO: CRUD

@router.post("", response_description="Create a new blog content", response_model=BlogContentResponse)
async def create_blog(blog_content: BlogContent, current_user = Depends(oath2.get_current_user)):
    try:
        blog_content = jsonable_encoder(blog_content)

        # TODO: add more info mation about blog content
        blog_content["author_name"] = current_user["name"]
        blog_content["author_id"] = current_user["_id"]
        blog_content["created_at"] = str(datetime.utcnow())

        new_blog_content = await db["blogPost"].insert_one(blog_content)

        created_blog_content = await db["blogPost"].find_one({"_id": new_blog_content.inserted_id})

        if created_blog_content:
            return created_blog_content
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Something wrong with post the blog"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )