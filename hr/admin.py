from django.contrib import admin

# Register your models here.
from hr.models import Staff, Project, Department, Role, Income, Expenditure

admin.site.register(Staff)
admin.site.register(Project)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Expenditure)
admin.site.register(Income)
