import jwt
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from database import engine
from models import Base
from fastapi import FastAPI, Request, Form
from database import engine, SessionLocal
from models import Base, User
import bcrypt
from auth import (
    create_access_token,
    verify_token
)
from fastapi.responses import RedirectResponse


app = FastAPI()

SECRET_KEY = "fitcheck_secret_key"

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

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@app.post("/login")
def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        db.close()
        return {
            "message": "User Not Found"
        }

    password_match = bcrypt.checkpw(
        password.encode(),
        user.password.encode()
    )

    db.close()

    if password_match:

     token = create_access_token(
        user.email
    )

    response = RedirectResponse(
        url="/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="access_token",
        value=token
    )

    return response

    return {
        "message": "Invalid Password"
    }

@app.get("/dashboard")
def dashboard(request: Request):

    token = request.cookies.get(
        "access_token"
    )

    if not token:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    try:
        verify_token(token)

    except:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )