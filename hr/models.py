from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Location(models.Model):
    code = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.location


class AllProject(models.Model):
    code = models.CharField(max_length=255, unique=True)
    project_name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="projects/", default="place.jpg")
    contact = models.CharField(max_length=255)
    status = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.project_name


class Department(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Role(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Staff(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL)
    contact = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    nin = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    staff_status = models.CharField(max_length=255, default="Inactive")
    image = models.ImageField(upload_to="profile/", default="logo.jpg")
    signature = models.ImageField(upload_to="profile/", default="default.png")
    joined_on = models.DateTimeField(auto_now=True)
    staff_responsibilities = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Expenditure(models.Model):
    code = models.CharField(max_length=6)
    staff = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(AllProject, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.CharField(max_length=255, null=True, blank=True)
    item = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_approved = models.CharField(max_length=255, null=True, blank=True)
    approved_by = models.CharField(max_length=255, null=True, blank=True)
    entered_on = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.item


class Income(models.Model):
    code = models.CharField(max_length=6)
    staff = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(AllProject, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.CharField(max_length=255, null=True, blank=True)
    item = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    # reason = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    entered_on = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    qty = models.IntegerField(default=0, blank=True, null=True)
    sub_total = models.IntegerField(default=0, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.item


class Inventory(models.Model):
    code = models.CharField(max_length=6)
    staff = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(AllProject, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.CharField(max_length=255, null=True, blank=True)
    qty = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    reference_copy = models.ImageField(upload_to="projects/photocopies", default="logo.jpg", null=True, blank=True)

    def __str__(self):
        return self.item


class AddStaffToProject(models.Model):
    code = models.CharField(max_length=6)
    staff = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(AllProject, blank=True, null=True, on_delete=models.SET_NULL)
    tasks_to_do = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)


class AuditTrail(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(AllProject, blank=True, null=True, on_delete=models.SET_NULL)
    action = models.TextField()
    date = models.DateTimeField(auto_now=True)
