from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel,field_validator

from app.models import TeacherModel

api = APIRouter()

class TeacherIn(BaseModel):
    name:str
    password:str = 'ttt'

    @field_validator('name')
    def name_check(cls,value):
        assert value.isalpha(),'name must be alpha'
        return value

@api.get('')
async def get_all_teachers():
    teachers = await TeacherModel.all()
    return teachers

@api.post('')
async def add_a_new_teacher(tch:TeacherIn):
    teacher = await TeacherModel.create(
        name = tch.name,
        password = tch.password
    )
    return teacher

@api.get('/{tid}')
async def get_a_teacher(tid:int):
    teacher = await TeacherModel.get(id=tid)
    return teacher

@api.put('/{tid}')
async def modify_a_teacher(tid:int,tch:TeacherIn):
    data = tch.model_dump()
    teacher = await TeacherModel.filter(id=tid).update(**data)
    return teacher

@api.delete('/{tid}')
async def delete_a_teacher(tid:int):
    teacher = await TeacherModel.filter(id=tid).delete()
    if not teacher:
        raise HTTPException(
            status_code=404,
            detail=f'teacher id {tid} is not found.'
        )
    return 1