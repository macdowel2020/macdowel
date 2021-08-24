from django.contrib import admin

# Register your models here.
from hr.models import Staff, Department, Role, Income, Expenditure, AllProject, Asset

admin.site.register(Staff)
admin.site.register(AllProject)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Expenditure)
admin.site.register(Income)
admin.site.register(Asset)
