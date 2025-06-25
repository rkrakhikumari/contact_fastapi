from fastapi import FastAPI
from database import Base, engine
from routes import user, contact


app = FastAPI()

Base.metadata.create_all(bind=engine)



app.include_router(user.router)
app.include_router(contact.router)






