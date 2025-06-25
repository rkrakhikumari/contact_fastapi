from fastapi import Depends, HTTPException, APIRouter
from schemas import ContactCreate
from database import SessionLocal
from models import Contact, User
from starlette import status#type:ignore
from typing import Annotated
from sqlalchemy.orm import  Session
from  .auth import get_current_user

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_contact(db: db_dependency, current_user: User = Depends(get_current_user)):
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).all()
    return contacts



@router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_contact(db:db_dependency, contact: ContactCreate, current_user: User = Depends(get_current_user)):
    new_contact = Contact(
        name = contact.name,
        email = contact.email,
        phone_num = contact.phone_num,
        note = contact.note,
        user_id = current_user.id
    )
    db.add(new_contact)


    db.commit()
    return {"msg": "Contact created"}





@router.put('/update/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_contact(db: db_dependency, contact: ContactCreate, contact_id: int, current_user: User = Depends(get_current_user)):
    contact_model = db.query(Contact).filter(Contact.id==contact_id, Contact.user_id == current_user.id).first()
    if not contact_model:
        raise HTTPException(status_code=404, detail='not found')
    contact_model.name = contact.name
    contact_model.email = contact.email
    contact_model.phone_num = contact.phone_num
    contact_model.note = contact.note
    db.commit()




@router.delete('/delete/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(db:db_dependency, contact_id: int, current_user: User = Depends(get_current_user)):
    contact_model = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if contact_model is None:
        raise HTTPException(status_code=404, detail= 'not found')
    db.delete(contact_model)
    db.commit()