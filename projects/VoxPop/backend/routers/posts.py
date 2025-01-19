from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.Post])
async def read_posts(
    limit: int | None = None,
    skip: int = 0,
    db: Session = Depends(get_db),
) -> list[schemas.Post]:
    """
    Retrieve all posts in chronological order (most recent first). 

    Args:
    - limit (int, optional): Limit the number of posts returned. Defaults to None.
    - skip (int, optional): Skip the first n posts. Defaults to 0.

    Returns:
    - list[schemas.Post]: A list of Post objects.
    """
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts



@router.get("/{post_id}", response_model=schemas.Post)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)) -> schemas.Post:
    """
    Retrieve a post by its ID.

    Args:
    - post_id (int): The ID of the post to retrieve.
    - db (Session): The database session.

    Returns:
    - schemas.Post: The Post object with the given ID.

    Raises:
    - HTTPException: If no post with the given ID exists.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  
async def create_post(
    post_create: schemas.PostCreate, db_session: Session = Depends(get_db)
) -> schemas.Post:
    """
    Creates a new post given the PostCreate object.

    Args:
    - post_create (schemas.PostCreate): The PostCreate object containing the post data.
    - db_session (Session): The database session dependency.

    Returns:
    - schemas.Post: The newly created Post object.
    """
    post = models.Post(**post_create.dict())
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post



@router.post("/{post_id}/like")
async def like_post(post_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Increment the like count for a post with the given ID.

    Args:
        post_id (int): The ID of the post to like.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the updated like count for the post.

    Raises:
        HTTPException: If no post with the given ID exists.
    """

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        post.likes += 1
        db.commit()
        return {"likes": post.likes}
    raise HTTPException(status_code=404, detail="Post not found")



