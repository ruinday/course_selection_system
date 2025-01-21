from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from app.models import GradeModel

api = APIRouter()

class GradeIn(BaseModel):
    name:str
    total:int = 70

@api.get('')
async def get_all_grades():
    grades = await GradeModel.all()
    return grades

@api.post('')
async def add_a_new_grade(grd:GradeIn):
    grade = await GradeModel.create(
        name = grd.name,
        total = grd.total
    )
    return grade

@api.get('/{gid}')
async def get_a_grade(gid:int):
    grade = await GradeModel.get(id=gid)
    return grade

@api.put('/{gid}')
async def modify_a_grade(gid:int,grd:GradeIn):
    data = grd.model_dump()
    grade = await GradeModel.filter(id=gid).update(**data)
    return grade

@api.delete('/{gid}')
async def delete_a_grade(gid:int):
    grade = await GradeModel.filter(id=gid).delete()
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f'grade id {gid} is not found.'
        )
    return 1