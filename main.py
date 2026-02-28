from fastapi import FastAPI, Path, Body, Depends, HTTPException
import models
from database import engine
from sqlalchemy.orm import Session
from typing import Annotated
from helpers import get_db
from starlette import status
from pydantic import BaseModel, Field
from enum import Enum

MEMBERS = [
    { "id": 1, "name": "Himanshu", "age": 26, "gender": "M", "marital_status": "unmarried"},
    { "id": 2, "name": "Vikash", "age": 25, "gender": "M", "marital_status": "unmarried"},
    { "id": 3, "name": "Vishal", "age": 22, "gender": "M", "marital_status": "unmarried"},
    { "id": 4, "name": "Shikha", "age": 22, "gender": "F", "marital_status": "unmarried"},
    { "id": 5, "name": "Maria", "age": 26, "gender": "F", "marital_status": "unmarried"},
    
]

class GenderEnum(str, Enum):
    M = "M"
    F = "F"
    O = "O"

class Member_Body(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(min= 18, max=60)
    gender: GenderEnum
    marital_status: str
    active: bool

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

# get method
@app.get("/members", status_code=status.HTTP_200_OK)
async def get_all_members(db: db_dependency):
    return db.query(models.Members).all()

@app.get("/members/{member_id}")
async def get_members_by_id(member_id: int = Path(gt=0)):
    for member in MEMBERS:
        if member.get("id") == member_id:
            return member
    else:
        return "Member with the given id is not present."
    
@app.post("/members/create-member")
async def create_new_member(new_member_request: Member_Body, db: db_dependency):
    try:
        member_model = models.Members(**new_member_request.model_dump())
        db.add(member_model)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.put("/members/update-member")
async def update_member(updated_member= Body()):
    for i in range(len(MEMBERS)):
        if MEMBERS[i].get("id") == updated_member.get("id"):
            MEMBERS[i] = updated_member
            return f"member with id {updated_member.get('id')} is updated successfully!"
    else:
        return "Member with the given id is not present."
    
@app.delete("/members/delete-member/{member_id}")
async def delete_member(member_id: int = Path(gt=0)):
    for i in range(len(MEMBERS)):
        if MEMBERS[i].get("id") == member_id:
            MEMBERS.pop(i)
            return f"Member with id {member_id} is deleted successfully!"
    else:
        return "Member with given id is not present."