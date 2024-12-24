from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlmodel import Session, select

from database import get_db
import otp, schemas, models
from SECRET_DATA import Email_Secrets

router = APIRouter(tags=["OTP-Actions"], prefix="/otp")

@router.get("/send/{email}")
def send(email):
    otp_to_send = otp.get_otp(email)
    send_otp(email, otp_to_send)

@router.post("/verify")
def verify_otp(request_body: schemas.OTPBody, db: Session = Depends(get_db)):
    check = otp.verify_otp(request_body.email, request_body.otp)
    if not check:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "OTP did not match"})
    
    user = db.exec(select(models.User).where(models.User.email == request_body.email)).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "server error"})
    user.is_active = True
    db.add(user)
    db.commit()
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "Account Created"})
    





def send_otp(receiver, otp_to_send):
    import smtplib
    sender = Email_Secrets.sender_email()
    subject = "OTP From RentEase."
    message = f"OTP is {otp_to_send},OTP will expire in 5 minutes.\nRentEase."

    text = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, Email_Secrets.app_pass())

    server.sendmail(sender, receiver, text)
