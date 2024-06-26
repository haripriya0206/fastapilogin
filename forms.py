from typing import Optional ,List
from fastapi import Request

class UserCreateForm:
    def __init__(self , request: Request):
        self.request : Request = request
        self.errors : List=[]
        self.username : Optional[str] = None
        self.email :Optional[str] = None
        self.password : Optional[str] = None


    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not len(self.username) >=4:
           self.errors.append("username contaion minimum 4 characters")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("please enter valid Email")
        if not self.password or not len (self.password) >= 4 : 
           self.errors.append("password contaion minimum 4 characters")
        if not self.errors:
            return True
        return False                  