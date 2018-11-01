from django.shortcuts import render
from .models import Triples
from kgqa.nl2sparql import NL2sparql


#主页面提供搜索框
def index(request):
    return render(request,'kgqa/index.html')
#设置数据接口可以提供数据下载
def schema(request):
    return render(request,'kgqa/schema.html')
#结果处理，将问题存入mysql数据库，对输入的问题进行解析。解析后生成echart网页，将网页呈现出来。
def result(request):
    query_question = request.POST["question"]
    Triples.objects.create(question = query_question)
    error_msg = ''
    ################
    #TODO:这里将query_question传给一个类用来搜索数据库，将结果用echart绘图。
    #首先该类将自然语言转成SPARQL
    #接着用该sparql去搜索数据库将搜索结果转成
    ###############
    if query_question:
        NL2sparql.question(query_question)
        return render(request, 'kgqa/render.html')
        # return render(request, 'kgqa/result.html',context={'error_msg':error_msg,"question":query_question})

    else:
        error_msg = "Please Enter Your Question!"
        return render(request,'kgqa/result.html',{'error_msg':error_msg})





