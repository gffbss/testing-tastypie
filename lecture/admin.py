from django.contrib import admin
from lecture.models import Class, Student, StudentProject
from uploadbox.models import Media


admin.site.register(Class)
admin.site.register(Student)
admin.site.register(StudentProject)
admin.site.register(Media)