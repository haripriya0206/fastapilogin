from fastapi import FastAPI, Request,Form,Depends
from fastapi.templating import Jinja2Templates
from forms import UserCreateForm
import models
from database import engine , SessionLocal
from sqlalchemy.orm  import Session
app = FastAPI()
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/')
def home( request : Request):
    return templates.TemplateResponse("loginpage.html", {"request":request})

@app.post('/signin')
def login(request : Request , email : str = Form(...) , password : str = Form(...), db: Session = Depends(get_db)): 
            userdetails = db.query(models.Userdata).filter(models.Userdata.email == email).first()
            if userdetails is None :
                 message = [" User was not exists"]
                 return templates.TemplateResponse("loginpage.html",{"request":request , "message":message})
            elif userdetails.password !=password :
                 message = ["please enter correct password"]
                 return templates.TemplateResponse("loginpage.html",{"request":request , "message":message})
            else : 
                message = ["user login successfully!"]
                return templates.TemplateResponse("successpage.html",{"request":request , "message":message})

    
@app.get('/register')
def get_register(request:Request):
     return templates.TemplateResponse("registerpage.html",{"request":request})    

@app.post('/register')
def register(request : Request ,username : str = Form(...), email : str = Form(...) , password : str = Form(...), db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    form.load_data()
    if form.is_valid():
            total_row = db.query(models.Userdata).filter(models.Userdata.email == email).first()
            print(total_row)
            if total_row == None:
                print("Save")
                users = models.Userdata(username=username, email=email, password=password)
                db.add(users)
                db.commit()
                message= ["User created successfully! Please Login "]
 
                return templates.TemplateResponse("loginpage.html",{"request":request ,"message":message })
            else: 
                message = ["The email has already been taken"] 
                return templates.TemplateResponse("registerpage.html", {"request":request , "message" : message})
          
    else: 
        message = form.errors
    return templates.TemplateResponse("registerpage.html", {"request":request , "message":message})
