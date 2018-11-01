#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""

from django.urls import path

from . import views

app_name="kgqa"
urlpatterns = [
    path('',views.index,name='index'),
    path('result/',views.result,name="result"),
    path('schema/',views.schema,name="schema"),
]



