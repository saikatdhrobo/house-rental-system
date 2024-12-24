from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from database import engine
from routers import registration, otp_actions, rents, signin


app = FastAPI(title="RentEase")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(registration.router)
app.include_router(otp_actions.router)
app.include_router(signin.router)
app.include_router(rents.router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine) #This will create the tables in database.
