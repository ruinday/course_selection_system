from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

from apis import student,grade,teacher,course
from settings import TORTOISE_ORM

app = FastAPI()

# 路由分发
app.include_router(student.api,prefix='/students',tags=['Students API'])
app.include_router(grade.api,prefix='/grades',tags=['Grades API'])
app.include_router(teacher.api,prefix='/teachers',tags=['Teachers API'])
app.include_router(course.api,prefix='/courses',tags=['Courses API'])

# DB配置
register_tortoise(app,config=TORTOISE_ORM)

# 中间件
@app.middleware('http')
async def fa(request:Request,call_next):
    # 请求代码
    response = await call_next(request)
    # 响应代码
    return response

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins = '*',
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

if __name__ == '__main__':
    uvicorn.run('app:app',reload=True)