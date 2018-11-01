from django.db import models

# Create your models here.
#这个与数据库直接相关，定义的每一个变量都是一个表的列名字
"""
编辑 models.py 文件，改变模型。
运行 python manage.py makemigrations 为模型的改变生成迁移文件。
运行 python manage.py migrate 来应用数据库迁移。
"""


class Triples(models.Model):
    question = models.CharField(max_length=200)
    def __str__(self):
        return self.question

