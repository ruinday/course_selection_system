from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from tortoise.expressions import F
from tortoise.transactions import in_transaction

from models import StudentModel,CourseModel,GradeModel

api = APIRouter()

# 请求体数据模型
class StudentIn(BaseModel):
    name:str
    password:str = 'sss'
    grade_id:int = 1
    courses:List[int] = [1]

@api.get('')
async def get_all_students():
    students = await StudentModel.all().values('id','name','grade__name','courses__name')
    return students

@api.post('')
async def add_a_new_student(stu:StudentIn):
    student = await StudentModel.create(
        name = stu.name,
        password = stu.password,
        grade_id = stu.grade_id
    )

    # 多对多关系绑定
    stu_courses = await CourseModel.filter(id__in=stu.courses)
    await student.courses.add(*stu_courses)

    # 班级现有人数+1
    await GradeModel.filter(id=stu.grade_id).update(count=F('count')+1)

    # 课程选修人数+1
    for cid in stu.courses:
        await CourseModel.filter(id=cid).update(count=F('count')+1)

    return student

@api.get('/{sid}')
async def get_a_student(sid:int):
    student = await StudentModel.get(id=sid)
    stu_courses = await student.courses.all().values('name','teacher__name')
    return {'student':student,'courses':stu_courses}

@api.put('/{sid}')
async def modify_a_student(sid:int,stu:StudentIn):
    data = stu.model_dump()

    try:
        async with in_transaction() as conn:
            student = await StudentModel.get(id=sid)

            # 修改班级现有人数
            grade = await student.grade
            if data['grade_id'] != grade.id:
                grade.count -= 1
                await grade.save(using_db=conn)

                await GradeModel.filter(id=data['grade_id']).update(count=F('count')+1)

            # 修改课程选修人数
            courses = await student.courses.all()
            courses_id = [crs.id for crs in courses]
            data_courses = data.pop('courses')

            if courses_id != data_courses:
                new_courses = [cid for cid in data_courses if cid not in courses_id]
                giveup_courses = [cid for cid in courses_id if cid not in data_courses]

                if giveup_courses != []:
                    for crs in courses:
                        if crs.id in giveup_courses:
                            crs.count -= 1
                            await crs.save(using_db=conn)

                for cid in new_courses:
                    await CourseModel.filter(id=cid).update(count=F('count')+1)

            # 修改学生课程（多对多）
            data_courses = await CourseModel.filter(id__in=data_courses)
            await student.courses.clear()
            await student.courses.add(*data_courses)
            
            # 修改学生基本信息
            student = await StudentModel.filter(id=sid).update(**data)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return student

@api.delete('/{sid}')
async def delete_a_student(sid:int):
    async with in_transaction() as conn:
        student = await StudentModel.get(id=sid)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f'Student id {sid} is not found.'
            )
        else:
            # 更新班级人数
            grade = await student.grade
            grade.count -= 1
            await grade.save(using_db=conn)

            # 更新课程人数
            courses = await student.courses.all()
            for course in courses:
                course.count -= 1
                await course.save(using_db=conn)

            await student.delete(using_db=conn)

    return 1