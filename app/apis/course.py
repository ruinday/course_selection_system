from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel,field_validator

from app.models import CourseModel

api = APIRouter()

class CourseIn(BaseModel):
    name:str
    total:int = 120
    teacher_id:int = 1

@api.get('')
async def get_all_courses():
    courses = await CourseModel.all()
    return courses

@api.post('')
async def add_a_new_course(crs:CourseIn):
    course = await CourseModel.create(
        name = crs.name,
        total = crs.total,
        teacher_id = crs.teacher_id
    )
    return course

@api.get('/{cid}')
async def get_a_course(cid:int):
    course = await CourseModel.get(id=cid)
    return course

@api.put('/{cid}')
async def modify_a_course(cid:int,crs:CourseIn):
    data = crs.model_dump()
    course = await CourseModel.filter(id=cid).update(**data)
    return course

@api.delete('/{cid}')
async def delete_a_course(cid:int):
    course = await CourseModel.filter(id=cid).delete()
    if not course:
        raise HTTPException(
            status_code=404,
            detail=f'course id {cid} is not found.'
        )
    return 1