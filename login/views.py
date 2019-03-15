# coding=utf-8
import os
from django.shortcuts import render
from django.shortcuts import redirect
import random
import json
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from login.models import Arithmetic
from login.models import MathSummary
import datetime

path = os.path.dirname(os.path.realpath(__file__))
log_path = path + os.sep + 'log' + os.sep


# 数学测试界面
def show(request):
    username = request.session.get("username")
    if username:
        print("session:", username)
        data = generateTest(request)
        json.dumps(data)
        return render(request, 'testMath.html', {'data': data})
    else:
        return render(request, 'login.html')


# 产生新的数学题目
def generateTest(request):
    username = request.session.get("username")
    n1 = random.randint(11, 100)
    n2 = random.randint(10, n1 - 1)
    s_p = '{0} - {1} ='.format(n1, n2)
    s_m = '{0} + {1} ='.format(n1, n2)
    if n1 % 2 == 0:
        s = s_p
        operation = '-'
        r_answer = n1 - n2
    else:
        s = s_m
        operation = '+'
        r_answer = n1 + n2
    data = {'operation': operation, 'body': s, 'result': r_answer, 'num1': n1, 'num2': n2,
            'which_angel': username}
    return data


# 处理小朋友提交的答案
def answer(request):
    result = str(request.body, 'utf-8')
    saveLog(result)
    data = generateTest(request)
    return HttpResponse(json.dumps(data), content_type='application/json')


# 登陆后的导引页面
def index(request):
    username = request.session.get("username")
    if username:
        return render(request, 'index.html')
    else:
        # 没有当前小朋友的seesion，跳转至登录页
        return render(request, 'login.html')


# 用户退出
def my_logout(request):
    del request.session['username']
    return redirect('/login/')


# 展示当天所有小朋友的做题情况
def summary(request):
    data = query_today(request)
    return render(request, 'summary.html', {"data": data})


# 查询当天所有小朋友的做题情况
def query_today(request):
    today = datetime.datetime.now().date()
    data = list(MathSummary.objects.filter(date=today))
    return data


# 展示当前登录小朋友的当天做题情况
def single(request):
    data = query_today_single(request)
    return render(request, "SingleForStudent.html", {"data": data})


# 查询当前登录小朋友的做题情况
def query_today_single(request):
    username = request.session.get("username")
    today = datetime.datetime.now().date()
    data = list(Arithmetic.objects.filter(which_angel=username, date=today))
    return data


# 老师界面，查询指定小朋友做题情况
def query_today_specific_single(which_angel):
    today = datetime.datetime.now().date()
    data = list(Arithmetic.objects.filter(which_angel=which_angel, date=today))
    for x in data:
        print(x)
    return data


# 查询所有小朋友的做题统计
def summary_detail(request):
    which_ange = request.GET.get("which_angel")
    print(which_ange)
    data = query_today_specific_single(which_ange)
    return render(request, "SingleSummary.html", {"data": data})


# 保存小朋友的做题情况
def saveLog(result):
    result = json.loads(result)
    today = datetime.datetime.now().date()

    a = Arithmetic(which_angel=result['whichAngel'],
                   date=result['date'],
                   score=result["score"],
                   elapsed_time=result['elapsed_time'],
                   results=result['result'],
                   body=result['body'],
                   answer=result['answer'],
                   operation=result['operation'])
    # 保存一条新的做题记录
    a.save()
    # 根据做题记录，更新MathSummary表
    if MathSummary.objects.filter(which_angel=a.which_angel, date=today):
        all_test = MathSummary.objects.get(which_angel=a.which_angel, date=today).total
        if a.score:
            right_num = MathSummary.objects.get(which_angel=a.which_angel, date=today).right
            ms = MathSummary.objects.get(which_angel=a.which_angel, date=today)
            ms.right = right_num + 1

        else:
            wrong_num = MathSummary.objects.get(which_angel=a.which_angel, date=today).wrong
            ms = MathSummary.objects.get(which_angel=a.which_angel, date=today)
            ms.wrong = wrong_num + 1
        ms.total = all_test + 1
    else:
        if a.score:
            ms = MathSummary.objects.create(which_angel=a.which_angel, total=1, date=today, right=1, wrong=0)
        else:
            ms = MathSummary.objects.create(which_angel=a.which_angel, total=1, date=today, right=0, wrong=1)
    ms.save()


# 用户注册
@csrf_exempt
def register(request):
    errors = []
    account = None
    password = None
    password2 = None
    email = None
    CompareFlag = False

    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('用户名不能为空')
            return render(request, 'register.html', {'errors': errors})
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors.append('密码不能为空')
            return render(request, 'register.html', {'errors': errors})
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('确认一下你的密码吧')
            return render(request, 'register.html', {'errors': errors})
        else:
            password2 = request.POST.get('password2')
        if password is not None:
            if password == password2:
                CompareFlag = True
            else:
                errors.append('两次输入的密码不一致')

        if account is not None and password is not None and password2 is not None and CompareFlag:
            count = User.objects.filter(username=account).count()
            if count > 0:
                errors.append('该用户名已经存在')
                return render(request, 'register.html', {'errors': errors})
            user = User.objects.create_user(account, email, password)
            user.save()
            userlogin = auth.authenticate(username=account, password=password)
            auth.login(request, userlogin)
            return redirect('/login/')
    return render(request, 'register.html', {'errors': errors})


# 用户登录
@csrf_exempt
def my_login(request):
    query_today(request)
    errors = []
    account = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('用户名不能为空')
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors = request.POST.get('密码不能为空')
        else:
            password = request.POST.get('password')

        if account is not None and password is not None:
            user = auth.authenticate(username=account, password=password)
            if user is not None:
                if user.is_active:
                    if user.username == "teacher":
                        request.session["username"] = user.username
                        return redirect('/summary')
                    auth.login(request, user)
                    print('account:', account)
                    request.session["username"] = user.username
                    return redirect('/index/')
                else:
                    errors.append('用户名错误')
            else:
                errors.append('用户名或密码错误')
    return render(request, 'login.html', {'errors': errors})
