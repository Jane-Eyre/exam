from django.db import models


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
