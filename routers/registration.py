from datetime import date
from fastapi.responses import JSONResponse
from sqlmodel import or_
import routers.dependencies as d
import hashing

router = d.APIRouter(tags=["Registration"])

@router.post("/user/", status_code=d.status.HTTP_201_CREATED)
def user_registration(request_body: d.schemas.UserSchema, db: d.Session = d.Depends(d.get_db)):
        check_user = db.exec(d.select(d.models.User).where(or_(d.models.User.email == request_body.email, d.models.User.contact == request_body.contact))).first()
        if check_user:
            return JSONResponse({"detail": "user is already registered"},status_code=400)
            # raise d.HTTPException(status_code=d.status.HTTP_400_BAD_REQUEST, detail="Already Registered")
        else:
            request_body.password = hashing.get_hashed_password(request_body.password)
            new_user = request_body.dict()
            new_user['ac_creation'] = get_current_date_time()
            new_user = d.models.User.model_validate(new_user)
            # new_user = d.models.User(first_name=request_body.first_name, last_name=request_body.last_name, email=request_body.email, password=request_body.password, ac_creation=get_current_date_time())

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            # return new_user

            return JSONResponse(status_code=d.status.HTTP_201_CREATED, content={'message': 'account created'})
            # raise d.HTTPException(status_code=d.status.HTTP_201_CREATED, detail="Registration Successful")
    




def get_current_date_time():
    return date.today()
