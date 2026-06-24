from django.contrib import admin
from .models import Student, Teacher, SchoolClass, Attendance, Grade

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(SchoolClass)
admin.site.register(Attendance)
admin.site.register(Grade)
