from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, UploadFile
from uuid import uuid4
import secrets
import string
import resend 
import os




def generate_email_verification_code(length=6):
    characters = string.ascii_letters + string.digits 
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_email_code_expiry(minutes=10):
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


async def send_verification_email(email: str, code: str):
    resend.api_key = str(os.getenv("RESEND_API_KEY"))

    try:
        params: resend.Emails.SendParams = {
            "from":"onboarding@resend.dev", 
            "to": email,
            "subject": "Verify your email",
            "html": f"<p>Your verification code is: <strong>{code}</strong></p>"
        } 
        email_response: resend.Email = resend.Emails.send(params)
        return email_response
    
    except Exception as e:
        print(f"Error sending email: {str(e)}") 
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    

def generate_password_forgot_code(length=6):
    characters = string.ascii_letters + string.digits  
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_password_forgot_code_expiry(minutes=10):
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)

async def send_password_reset_email(email: str, code: str):
    resend.api_key = str(os.getenv("RESEND_API_KEY"))

    try:
        params: resend.Emails.SendParams = {
            "from": "onboarding@resend.dev",  
            "to": email,
            "subject": "Reset Your Password",
            "html": f"""
                <p>You requested a password reset.</p>
                <p>Your verification code is: <strong>{code}</strong></p>
                <p>If you did not request this, please ignore this email.</p>
            """
        } 
        email_response: resend.Email = resend.Emails.send(params)
        # Return the email response or a success message
        return {"message": "Password reset email sent successfully", "response": email_response}

    except Exception as e:
        error_message = f"Error sending password reset email: {str(e)}"
        print(error_message)  # Better logging
        raise HTTPException(status_code=500, detail="Failed to send password reset email")

    
MEDIA_DIR = "app/media"
def save_file(file: UploadFile, subdir: str = "") -> str:
    os.makedirs(f"{MEDIA_DIR}/{subdir}", exist_ok=True)
    ext = file.filename.split(".")[-1]
    unique_name = f"{uuid4().hex}.{ext}"
    path = os.path.join(MEDIA_DIR, subdir, unique_name)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())
    return path 

