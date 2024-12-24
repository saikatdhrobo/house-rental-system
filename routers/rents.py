from fastapi import APIRouter,status, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from database import get_db
import models, schemas, Oauth2

router = APIRouter(prefix='/rents', tags=["Rents"])

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_rent(ad_body: schemas.RentRequestBody, db: Session = Depends(get_db), current_user = Depends(Oauth2.get_current_user)):
    new_ad = dict(ad_body)
    new_ad['user_id'] = current_user.id
    new_ad = models.Rents.model_validate(new_ad)

    db.add(new_ad)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'message': 'rent posted'})


@router.get('/all', response_model=list[schemas.AdResponseSchema])
def read_all_rents(db: Session = Depends(get_db)):
    results = db.exec(select(models.Rents)).all()
    return results


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_rent(id, db: Session = Depends(get_db)):
    result = db.exec(select(models.Rents).where(models.Rents.id == id)).first()
    
    db.delete(result)
    db.commit()