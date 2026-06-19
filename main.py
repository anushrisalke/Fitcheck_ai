from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from database import engine
from models import Base
from fastapi import FastAPI, Request, Form
from database import engine, SessionLocal
from models import Base, User
import bcrypt



app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Welcome to FitCheck AI"}

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )

@app.post("/register")
def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.add(user)

    db.commit()

    db.close()

    return {
        "message": "User Registered Successfully"
    }