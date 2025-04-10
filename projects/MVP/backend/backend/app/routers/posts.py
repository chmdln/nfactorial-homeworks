from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database.models import User, Post, Like, Comment
from app.database.database import get_db
from app.auth import get_current_user 

from app.schemas import (   
    PostCreateResponse, PostEditResponse,
    PostLikeResponse, PostUnlikeResponse, 
    PostCommentResponse, PostCommentRequest, 
    EditPostCommentRequest, EditPostCommentResponse
)

from app.utils import save_file 



load_dotenv()

router = APIRouter(
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/feed", response_model=list[PostCreateResponse])
async def get_feed(
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    posts = (db.query(Post).filter(Post.user_id != user.id)
            ).order_by(Post.created_at.desc()).all()

    for post in posts:
        post.comments.sort(key=lambda comment: comment.created_at, reverse=True)

    if not posts:
        return []
    return posts
    

@router.get("/feed/posts", response_model=list[PostCreateResponse])
async def get_all_posts(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    for post in posts:
        post.comments.sort(key=lambda comment: comment.created_at, reverse=True)
    return posts 


@router.post("/feed/posts", status_code=status.HTTP_201_CREATED, response_model=PostCreateResponse)
async def create_post(
    content: str = Form(...), 
    uploaded_file: UploadFile = File(None), 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)  
):
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post content is required"
        )
    
    if uploaded_file:
        file_path = save_file(uploaded_file, subdir="posts")

    try:
        new_post = Post(
            content=content,
            media_url=file_path if uploaded_file else None,  
            user_id=user.id
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)  
        return new_post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the post: {str(e)}"
        )

    

@router.put("/feed/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=PostEditResponse)
async def edit_post(
    post_id: str,
    content: str = Form(...),
    uploaded_file: UploadFile = File(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you do not have permission to edit this post"
        )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post content is required"
        )
    
    if uploaded_file:
        file_path = save_file(uploaded_file, subdir="posts")
        post.media_url = file_path if uploaded_file else None

    post.content = content
    db.commit()
    return post 


@router.delete("/feed/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you do not have permission to delete this post"
        )
    db.delete(post)
    db.commit() 


@router.post(
        "/feed/posts/{post_id}/like", 
        status_code=status.HTTP_200_OK, 
        response_model=PostLikeResponse
)
async def like_post(
    post_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )

    existing_like = (
        db.query(Like)
        .filter(Like.post_id == post_id, Like.user_id == user.id)
        .first()
    )
    if existing_like:
        print("User has already liked this post")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You have already liked this post"
    )

    if post.user_id == user.id:
        print("User cannot like their own post")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You cannot like your own post"
    )

    like = Like(post_id=post.id, user_id=user.id)
    db.add(like)
    db.commit()
    db.refresh(post)
    return post
    

@router.delete(
        "/feed/posts/{post_id}/like", 
        status_code=status.HTTP_200_OK, 
        response_model=PostUnlikeResponse
)    
async def unlike_post(
    post_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user.id).first()
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Like not found"
        )
    db.delete(like)
    db.commit()
    db.refresh(post)
    return post 


@router.post(
        "/feed/posts/{post_id}/comments", 
        status_code=status.HTTP_201_CREATED,
        response_model=PostCommentResponse
)
async def comment_post(
    post_id: str,
    comment: PostCommentRequest, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )

    comment = Comment(post_id=post.id, user_id=user.id, content=comment.content)
    db.add(comment)
    db.commit()
    db.refresh(post)
    return comment 


@router.put(
    "/feed/posts/{post_id}/comments/{comment_id}",
    status_code=status.HTTP_200_OK,  
    response_model=EditPostCommentResponse
)
async def edit_post_comment(
    post_id: str,
    comment_id: str,
    content: EditPostCommentRequest,  
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if comment.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own comments"
        )

    comment.content = content.content 
    db.commit()
    db.refresh(comment) 
    return comment  



@router.delete(
    "/feed/posts/{post_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_comment(
    post_id: str,
    comment_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    comment = db.query(Comment).filter(post.id == post_id, Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if comment.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )

    db.delete(comment)
    db.commit()    
