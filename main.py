from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import  Session
from database import SessionLocal
from starlette import status#type:ignore
from pydantic import BaseModel, Field
from models import Contact
from database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



class ContactRequest(BaseModel):
    name : str = Field(min_length=3),
    email : str 
    phone_num : str
    note : str



@app.get('/', status_code=status.HTTP_200_OK)
async def get_all_contact(db: db_dependency):
    return db.query(Contact).all()



@app.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_contact(db:db_dependency, contact: ContactRequest):
    new_contact = Contact(
        name = contact.name,
        email = contact.email,
        phone_num = contact.phone_num,
        note = contact.note
    )
    db.add(new_contact)


    db.commit()




@app.put('/update/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_contact(db: db_dependency, contact: ContactRequest, contact_id: int):
    contact_model = db.query(Contact).filter(Contact.id==contact_id).first()
    if not contact_model:
        raise HTTPException(status_code=404, detail='not found')
    contact_model.name = contact.name
    contact_model.email = contact.email
    contact_model.phone_num = contact.phone_num
    contact_model.note = contact.note
    db.commit()




@app.delete('/delete/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(db:db_dependency, contact_id: int):
    contact_model = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact_model is None:
        raise HTTPException(status_code=404, detail= 'not found')
    db.delete(contact_model)
    db.commit()