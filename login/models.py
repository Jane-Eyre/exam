from django.db import models
import datetime

class Arithmetic(models.Model):
    which_angel = models.CharField(max_length=20)
    body = models.CharField(max_length=100)
    answer = models.IntegerField()
    score = models.BooleanField(max_length=None)
    elapsed_time = models.CharField(max_length=10)
    results = models.IntegerField()
    operation = models.CharField(max_length=3)
    date = models.DateField(max_length=30)

    # def __init__(self, which_angel, date, score, elapsed_time, results, body, answer, operation):
    #     super().__init__()
    #     self.which_angel = which_angel
    #     self.date = date
    #     self.score = score
    #     self.elapsed_time = elapsed_time
    #     self.results = results
    #     self.body = body
    #     self.answer = answer
    #     self.operation = operation


class MathSummary(models.Model):
    which_angel = models.CharField(max_length=20)
    wrong = models.IntegerField()
    right = models.IntegerField()
    total = models.IntegerField()
    date = models.DateField(max_length=10)


# 应用题生成
class GenerateProblems(models.Model):
    scene = models.CharField(max_length=20)
    background = models.CharField(max_length=100)
    quantifier = models.CharField(max_length=20)
    obj = models.CharField(max_length=20)
    activity = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    n1 = models.IntegerField()
    n2 = models.IntegerField()
    op = models.CharField(max_length=10)
    res = models.CharField(max_length=10)

    def __str__(self):
        return "%s the g_problem at %s" % (self.scene, self.background)


# 应用题表
class Problems(models.Model):
    body = models.CharField(max_length=100)
    problem = models.OneToOneField(
        GenerateProblems,
        on_delete=models.CASCADE,
        null=True
    )
    which_angel = models.CharField(max_length=20, null=True)
    answer = models.IntegerField(null=True)
    score = models.BooleanField(max_length=None, null=True)
    elapsed_time = models.CharField(max_length=10, null=True)
    results = models.IntegerField(null=True)
    operation = models.CharField(max_length=3, null=True)
    date = models.DateField(max_length=30, null=True)

    def __str__(self):
        return "%s the problem" % self.body

