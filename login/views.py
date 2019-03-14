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
import datetime

path = os.path.dirname(os.path.realpath(__file__))
log_path = path + os.sep + 'log' + os.sep


def show(request):
    username = request.session.get("username")
    if username:
        print("session:", username)
        data = generateTest(request)
        json.dumps(data)
        return render(request, '../static/testMath.html.backup', {'data': data})
    else:
        return render(request, 'login.html')


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


def answer(request):
    result = str(request.body, 'utf-8')
    print("result:", result)
    saveLog(result)
    data = generateTest(request)
    print("new data:", data)
    return HttpResponse(json.dumps(data), content_type='application/json')


def index(request):
    username = request.session.get("username")
    if username:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')


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
    queryToday(request)
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
                    auth.login(request, user)
                    print('account:', account)
                    request.session["username"] = user.username
                    return redirect('/index/')
                else:
                    errors.append('用户名错误')
            else:
                errors.append('用户名或密码错误')
    return render(request, 'login.html', {'errors': errors})


# 用户退出
def my_logout(request):
    del request.session['username']
    return redirect('/login/')


def summary(request):
    return render(request, 'summary.html')


def saveLog(result):
    result = json.loads(result)

    a = Arithmetic(which_angel=result['whichAngel'],
                   date=result['date'],
                   score=result["score"],
                   elapsed_time=result['elapsed_time'],
                   results=result['result'],
                   body=result['body'],
                   answer=result['answer'],
                   operation=result['operation'])
    a.save()


def queryToday(request):
    today = datetime.datetime.now().date()
    for e in Arithmetic.objects.all():
        print(e.date)
