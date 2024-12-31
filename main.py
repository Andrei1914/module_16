from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import FastAPI, Path
from typing import Annotated
from fastapi.templating import Jinja2Templates
temp = Jinja2Templates(directory="templates")

app = FastAPI()

users_db = []


class Users(BaseModel):
    id: int = None
    user_name: str
    age: int = None

@app.get('/')
async def all_users(request: Request) -> HTMLResponse:
    return temp.TemplateResponse("users.html", {"request":request, "users":users_db})

@app.get('/user/{user_id}')
async def get_user(request: Request, user_id:int) -> HTMLResponse:
    try:
        return temp.TemplateResponse("users.html", {"request":request, "users_id":users_db[user_id]})
    except IndexError:
        HTTPException(status_code=404, detail="Not user id")

@app.post('/', status_code=status.HTTP_201_CREATED)
async def post_message(request: Request, username: str = Form(), age: int = Form()) -> HTMLResponse:
    new_id = max((i.id for i in users_db), default=0) + 1
    new_user = Users(id=new_id, user_name=username, age=age)
    users_db.append(new_user)
    return temp.TemplateResponse("users.html", {"request":request, "users":users_db})

@app.put('/update_users/{user_id}', response_model=Users)
async def put_message(users_id: Annotated[int, Path(
                            ge=1,
                            example="Enter your id"
                            )],
                        username: Annotated[str, Path(
                            min_length=3,
                            max_length=10,
                            example="Enter your username"
                            )],
                        age: Annotated[str, Path(
                            ge=16,
                            le=100,
                            example="Enter your age"
                        )]):
    try:
        for m in users_db:
            if m.id == users_id:
                m.age = age
                return m.id
    except IndexError:
        HTTPException(status_code=404, detail="Not message id")

@app.delete('/delete_message/{message_id}')
async def put_message(message_id: Annotated[int, Path(
                            ge=1,
                            example="Enter id your message to read"
                            )]):
    try:
        for i, m in enumerate(users_db):
            if i == message_id:
               del users_db[i]
            return f"{users_db[i]} delete!"
    except IndexError:
        HTTPException(status_code=404, detail="Not message id")


