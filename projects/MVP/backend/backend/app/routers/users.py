from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime, timezone
import os 

from app.schemas import (
    UserCreateRequest, UserCreateResponse, 
    UserLoginRequest, UserLoginResponse, 
    UserGetResponse,  UserResetPasswordCodeRequest, 
    UserResetPasswordRequest, UserPersonalizeProfileRequest,
    UserPersonalizeProfileResponse 
)
from app.database.database import get_db
from app.database.models import (
    User, EmailVerificationCode, 
    PasswordForgotCode
)
from app.utils import (
    get_email_code_expiry, generate_email_verification_code,
    send_verification_email, generate_password_forgot_code, 
    get_password_forgot_code_expiry, send_password_reset_email
)

from app.auth import (
    create_access_token, hash_password, verify_password, 
    get_current_user
)

load_dotenv()

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/auth/signup",  status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse) 
async def signup(user: UserCreateRequest, db: Session = Depends(get_db)):
    try: 
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="User with this email already exists"
            )
    
        hashed_password = hash_password(user.password)
        new_user = User(
            email=user.email, 
            hashed_password=hashed_password,  
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user) 

        access_token = create_access_token(data={"sub": new_user.email})
        return { "access_token": access_token, "token_type": "bearer" }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
    

@router.get("/users/me", status_code=status.HTTP_200_OK, response_model=UserGetResponse)
async def get_user(user: User = Depends(get_current_user)):
    return user 


@router.get("/auth/verify-email", status_code=status.HTTP_200_OK)
async def send_email_verification_token(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        existing_code = db.query(EmailVerificationCode).filter(EmailVerificationCode.user_id == user.id).first()
        if existing_code:
            db.delete(existing_code)

        email_verification_code = generate_email_verification_code()
        email_verification_code_expires_at=get_email_code_expiry()
        code = EmailVerificationCode(
            user_id=user.id, 
            code=email_verification_code,
            expires_at = email_verification_code_expires_at,
        )

        db.add(code)
        email = await send_verification_email(user.email, email_verification_code) 
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Verification code sent to {email}"}
        )  

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


@router.post("/auth/verify-email", status_code=status.HTTP_200_OK) 
async def verify_email(token: str, db: Session = Depends(get_db)):
    valid_token = db.query(EmailVerificationCode).filter(
        EmailVerificationCode.code == token
    ).first()

    if not valid_token:
        raise HTTPException(status_code=404, detail="Verification code not found")

    if valid_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        db.delete(valid_token) 
        db.commit()
        raise HTTPException(status_code=400, detail="Verification code has expired")

    user = db.query(User).filter(User.id == valid_token.user_id).first()
    if not user:
        db.delete(valid_token)
        db.commit()
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_verified = True
    db.delete(valid_token)
    db.commit()
    return {"message": "Email successfully verified. You can now log in."}


@router.put("/auth/profile/", status_code=status.HTTP_200_OK, response_model=UserPersonalizeProfileResponse)
async def personalize_profile(
    data: UserPersonalizeProfileRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Personalize the user profile after signup.
    """
    if user.is_profile_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile has already been completed."
        )

    try:
        for field in ["first_name", "last_name", "company", "position", "location"]:
            setattr(user, field, getattr(data, field))

        user.is_profile_complete = True
        db.commit()
        db.refresh(user)
        return user

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating your profile."
        ) from e

   

@router.post("/auth/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def login(user: UserLoginRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )   
    
    access_token = create_access_token(data={"sub": existing_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post("/auth/password-reset-code", status_code=status.HTTP_200_OK)
async def send_password_reset_code(
    data: UserResetPasswordCodeRequest, 
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not verified. Please verify your email first."
        )

    try:
        existing_code = db.query(PasswordForgotCode).filter(PasswordForgotCode.user_id == user.id).first()
        if existing_code:
            db.delete(existing_code)
            db.commit() 

        password_forgot_code = generate_password_forgot_code()
        password_forgot_code_expires_at = get_password_forgot_code_expiry()

        new_code = PasswordForgotCode(
            user_id=user.id, 
            code=password_forgot_code,
            expires_at=password_forgot_code_expires_at,
        )

        db.add(new_code)
        db.commit()

        background_tasks.add_task(send_password_reset_email, user.email, password_forgot_code)
        return {"message": f"Password reset code sent to {user.email}"}

    except Exception as e:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the request."
        ) from e



@router.post("/auth/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: UserResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        code = db.query(PasswordForgotCode).filter(PasswordForgotCode.code == data.code).first()
        if not code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password reset code not found"
            )

        if code.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password reset code has expired"
            )

        user = db.query(User).filter(User.id == code.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.hashed_password = hash_password(data.password)
        db.commit()
        db.delete(code)
        db.commit()
        return {"message": "Password reset successfully"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the request."
        ) from e



