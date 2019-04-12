from django.contrib import admin

# Register your models here.
from . import models

from .models import GenerateProblems, Problems
admin.site.register(GenerateProblems)
admin.site.register(Problems)
