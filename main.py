import jwt
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from database import engine
from models import Base
from fastapi import FastAPI, Request, Form
from database import engine, SessionLocal
from models import Base, User,Analysis
from scraper import get_product_data
import bcrypt
from auth import (
    create_access_token,
    verify_token
)
from fastapi.responses import RedirectResponse


app = FastAPI()

SECRET_KEY = "fitcheck_ai_super_secret_key_2026"

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

@app.get("/logout")
def logout():

    response = RedirectResponse(
        url="/login",
        status_code=303
    )

    response.delete_cookie(
        key="access_token"
    )

    return response

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

@app.get("/analyze")
def analyze_page(request: Request):

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
        name="analyze.html"
    )

@app.post("/analyze")
def analyze_product(
    request: Request,
    product_url: str = Form(...)
):

    token = request.cookies.get(
        "access_token"
    )

    payload = verify_token(token)

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    data = get_product_data(
        product_url
    )

    analysis = Analysis(
        user_id=user.id,
        url=product_url,
        product_name=data["product_name"],
        price=data["price"],
        rating=data["rating"]
    )

    db.add(analysis)

    db.commit()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "url": product_url,
            "product_name": data["product_name"],
            "price": data["price"],
            "rating": data["rating"]
        }
    )

@app.get("/history")
def history_page(request: Request):

    token = request.cookies.get(
        "access_token"
    )

    if not token:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    payload = verify_token(token)

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    analyses = db.query(Analysis).filter(
        Analysis.user_id == user.id
    ).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "analyses": analyses
        }
    )