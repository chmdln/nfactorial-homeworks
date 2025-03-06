from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Annotated

from app.database.models import Listing, Comment, User, Favorite
from app.database.database import get_db
from app.auth import get_current_user
from app.schemas import (
    ListingPostRequest, ListingPostResponse, 
    ListingGetResponse, ListingUpdateRequest, 
    CommentsResponse, CommentPostRequest, 
    CommentUpdateRequest, FavoriteListingResponse,
    FavoriteListingsResponse, ListingFilter, 
    ListingsGetAllResponse
)




router = APIRouter(tags=["Listings"])

@router.post("/shanyraks", status_code=status.HTTP_200_OK, response_model=ListingPostResponse)
def create_listing(
    listing: ListingPostRequest, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):

    new_listing = Listing(**listing.dict())
    new_listing.owner = user 
   
    db.add(new_listing) 
    db.commit()     
    db.refresh(new_listing)
    return new_listing 



@router.get("/shanyraks/{id}", status_code=status.HTTP_200_OK, response_model=ListingGetResponse)
def get_listings(
    id: int, 
    db: Session = Depends(get_db)):
    existing_listing = db.query(Listing).filter(Listing.id == id).first()
    if not existing_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    return existing_listing



@router.patch("/shanyraks/{id}", status_code=status.HTTP_200_OK, response_class=Response)
def update_listing(
    id: int, 
    listing: ListingUpdateRequest, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):    
    existing_listing = db.query(Listing).filter(Listing.id == id).first()
    if not existing_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )

    # only listing owner can update it
    if existing_listing.owner != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this listing",
        )
    
    data = listing.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(existing_listing, key, value)

    db.commit()
    db.refresh(existing_listing)
    return Response(status_code=status.HTTP_200_OK)



@router.delete("/shanyraks/{id}", response_class=Response)
def delete_listing(
    id: int, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_listing = db.query(Listing).filter(Listing.id == id).first()
    if not existing_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    
    # only listing owner can delete it
    if existing_listing.owner != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this listing",
        )
    
    db.delete(existing_listing), 
    db.commit()
    return Response(
        status_code=status.HTTP_200_OK
)



@router.post("/shanyraks/{id}/comments", status_code=status.HTTP_200_OK, response_class=Response)
def create_comment(
    id: int, 
    user: User = Depends(get_current_user),
    comment: CommentPostRequest = Depends(),
    db: Session = Depends(get_db)
):
    existing_listing = db.query(Listing).filter(Listing.id == id).first()
    if not existing_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    
    new_comment = Comment(**comment.dict())
    new_comment.owner = user
    new_comment.listing = existing_listing
    existing_listing.total_comments += 1

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return Response(status_code=status.HTTP_200_OK) 



@router.get("/shanyraks/{id}/comments", 
            status_code=status.HTTP_200_OK, 
            response_model=CommentsResponse
    )   
def get_comments(
    id: int, 
    db: Session = Depends(get_db)
):
    listing = db.query(Listing).filter(Listing.id == id).first()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    return CommentsResponse(comments=listing.comments) 



@router.patch("/shanyraks/{id}/comments/{comment_id}", 
           status_code=status.HTTP_200_OK, 
           response_class=Response
    )
def update_comment(
    id: int, 
    comment_id: int, 
    comment: CommentUpdateRequest, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id, Comment.listing_id == id)
        .first()
    )

    if not existing_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    
    # only author of the comment can update it
    if existing_comment.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this comment",
        )

    data = comment.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(existing_comment, key, value)

    db.commit()
    db.refresh(existing_comment)
    return Response(status_code=status.HTTP_200_OK)




@router.delete("/shanyraks/{id}/comments/{comment_id}", 
           status_code=status.HTTP_200_OK, 
           response_class=Response
    )
def delete_comment(
    id: int, 
    comment_id: int, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id, Comment.listing_id == id)
        .first()
    )

    if not existing_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    
    # only author of the comment can delete it
    if existing_comment.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this comment",
        )
    
    existing_listing = db.query(Listing).filter(Listing.id == id).first()
    existing_listing.total_comments -= 1
    db.delete(existing_comment)
    db.commit()
    return Response(status_code=status.HTTP_200_OK) 



@router.post("/auth/users/favorites/shanyraks/{id}", 
             status_code=status.HTTP_200_OK, 
             response_class=Response
    )
def add_to_favorites(
    id: int,
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    existing_listing = db.query(Listing).filter(Listing.id == id).first()
    if not existing_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    
    # check if listing is already in favorites
    existing_favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id, Favorite.listing_id == id)
        .first()
    )

    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listing already in favorites",
        )

    new_favorite = Favorite(
        user_id=user.id, 
        listing_id=existing_listing.id, 
        address=existing_listing.address 
    )

    db.add(new_favorite)
    db.commit() 
    db.refresh(new_favorite)
    return Response(status_code=status.HTTP_200_OK)



@router.get("/auth/users/favorites/shanyraks", 
            status_code=status.HTTP_200_OK, 
            response_model=FavoriteListingsResponse)
def get_favorites(user: User = Depends(get_current_user)):
    favorites = user.favorites
    listings = [
        FavoriteListingResponse(
            id=favorite.listing_id, 
            address=favorite.address
        ) for favorite in favorites
    ]
    return FavoriteListingsResponse(shanyraks=listings)  



@router.delete("/auth/users/favorites/shanyraks/{id}", 
                status_code=status.HTTP_200_OK, 
                response_class=Response
    )    
def delete_favorite(
    id: int, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    existing_favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id, Favorite.listing_id == id)
        .first()        
    )

    if not existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found",
        )

    db.delete(existing_favorite)
    db.commit()
    return Response(status_code=status.HTTP_200_OK) 




@router.get("/shanyraks", response_model=ListingsGetAllResponse)  
def get_all_listings(
    data: Annotated[ListingFilter, Depends()],
    db: Session = Depends(get_db)
):
    query = db.query(Listing)
    
    if data.type:
        query = query.filter(Listing.type == data.type)
    if data.rooms_count:
        query = query.filter(Listing.rooms_count == data.rooms_count)
    if data.price_from is not None:
        query = query.filter(Listing.price >= data.price_from)
    if data.price_until is not None:
        query = query.filter(Listing.price <= data.price_until)
    
    listings = (
        query.order_by(Listing.created_at.desc())
        .offset(data.offset)
        .limit(data.limit)
        .all()
    )
    
    return {
        "total": len(listings),
        "listings": [
            {
                "id": l.id,
                "type": l.type,
                "price": l.price,
                "address": l.address,
                "area": l.area,
                "rooms_count": l.rooms_count,
            }
            for l in listings
        ]
    }





 