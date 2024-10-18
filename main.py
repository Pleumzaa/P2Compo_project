from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import hashlib

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User database model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # 'student' or 'teacher'
    subject = Column(String, nullable=True)
    section = Column(String, nullable=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI(debug=True)

# Mount the static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hash password utility
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Dictionary to store registered user data
registered_users = []

# Routes
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password_hash != hash_password(password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if user.role == "teacher":
        if user.subject == "introduction to algorithms":
            return RedirectResponse(url="/algorithm", status_code=303)
        elif user.subject == "feedback control":
            return RedirectResponse(url="/feedback", status_code=303)
        elif user.subject == "advanced computer programming for RAI":
            return RedirectResponse(url="/advanced-compro", status_code=303)
        else:
            raise HTTPException(status_code=400, detail="Subject not found")
    elif user.role == "student":
        return RedirectResponse(url="/alreadylog", status_code=303)
    else:
        raise HTTPException(status_code=400, detail="Role not recognized")

@app.get("/register/{role}", response_class=HTMLResponse)
async def registration_page(request: Request, role: str):
    if role not in ["student", "teacher"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    return templates.TemplateResponse(f"testRegisterS.html" if role == "student" else "testRegisT.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    name: str = Form(...),
    surname: str = Form(...),
    user_id: int = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    section: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a dictionary with the form data
    user_data = {
        "id": user_id,
        "name": f"{name} {surname}",
        "email": email,
        "password": hash_password(password),  # Store hashed password
        "section": section
    }

    # Add the user data to the registered_users list
    registered_users.append(user_data)

    # Create a new User instance for the database
    new_user = User(
        name=name,
        surname=surname,
        email=email,
        password_hash=user_data["password"],
        role="student",
        section=section
    )

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Redirect to the "already registered" page
    return RedirectResponse(url="/alreadyregis", status_code=303)

@app.get("/users", response_class=HTMLResponse)
async def get_users():
    # Display the registered users
    response = "<h2>Registered Users:</h2><ul>"
    for user in registered_users:
        response += f"<li>ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Section: {user['section']}</li>"
    response += "</ul>"
    return response

@app.get("/algorithm", response_class=HTMLResponse)
async def algorithm_page(request: Request):
    return templates.TemplateResponse("algo.html", {"request": request})

@app.get("/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request):
    return templates.TemplateResponse("CheackA.html", {"request": request})

@app.get("/advanced-compro", response_class=HTMLResponse)
async def advanced_compro_page(request: Request):
    return templates.TemplateResponse("checkAcompro.html", {"request": request})

@app.get("/alreadylog", response_class=HTMLResponse)
async def already_logged_in_page(request: Request):
    return templates.TemplateResponse("alreadylog.html", {"request": request})

# Route for test.S.html
@app.get("/role", response_class=HTMLResponse)
async def test_s_page(request: Request):
    return templates.TemplateResponse("test.S.html", {"request": request})

# Route for testRegisT.html
@app.get("/testRegisT", response_class=HTMLResponse)
async def test_register_teacher_page(request: Request):
    return templates.TemplateResponse("testRegisT.html", {"request": request})

# Route for testRegisterS.html
@app.get("/testRegisterS", response_class=HTMLResponse)
async def test_register_student_page(request: Request):
    return templates.TemplateResponse("testRegisterS.html", {"request": request})

@app.get("/alreadyregis", response_class=HTMLResponse)
async def already_registered_page(request: Request):
    return templates.TemplateResponse("alreadyregis.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
