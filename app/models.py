from tortoise import fields
from tortoise.models import Model

# region 基类
class AbstractModel(Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True     # 抽象模型，不生成表

class MixinTimeField:
    # 添加数据时间
    created = fields.DatetimeField(null=True,auto_now_add=True)
    # 修改数据时间
    modified = fields.DatetimeField(null=True,auto_now=True)

# endregion

class StudentModel(Model,MixinTimeField):
    name = fields.CharField(max_length=32)
    password = fields.CharField(max_length=12)

    grade = fields.ForeignKeyField('models.GradeModel',related_name='student')
    courses = fields.ManyToManyField('models.CourseModel',related_name='student')

    class Meta:
        table = 'students'
        # unique_together = ('',)
        ordering = ('name',)

class GradeModel(Model,MixinTimeField):
    name = fields.CharField(max_length=32)
    total = fields.IntField(default=40)
    count = fields.IntField(default=0)

    class Meta:
        table = 'grades'
        unique_together = ('name',)
        ordering = ('name',)

class CourseModel(Model,MixinTimeField):
    name = fields.CharField(max_length=32)
    total = fields.IntField(default=120)
    count = fields.IntField(default=0)

    teacher = fields.ForeignKeyField('models.TeacherModel',related_name='course')

    class Meta:
        table = 'courses'
        ordering = ('name',)

class TeacherModel(Model,MixinTimeField):
    name = fields.CharField(max_length=32)
    password = fields.CharField(max_length=12)
    is_admin = fields.BooleanField(default=False)

    class Meta:
        table = 'teachers'
        ordering = ('name',)