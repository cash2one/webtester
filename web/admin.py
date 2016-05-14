from django.contrib import admin
from model.case import Case
from model.testpost import TestPost
from model.action import Action
from model.check import Check
from model.report import Report

# Register your models here.
admin.site.register(Case)
admin.site.register(TestPost)
admin.site.register(Action)
admin.site.register(Check)
admin.site.register(Report)