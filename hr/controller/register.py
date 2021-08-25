import random
import string
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Staff, Department, Role, AuditTrail, AllProject


def update_staff_photo(incoming):
    if incoming.user.is_authenticated:
        if incoming.method == 'POST' and incoming.FILES['image']:
            email = incoming.GET['email']
            ustaff = Staff.objects.get(user__email__contains=email)
            image = incoming.FILES['image']
            print(image.name)
            print(image.size)

            Staff.objects.filter(user__email__contains=ustaff.user.email).update(
                image=image
            )
            fs = FileSystemStorage()
            fs.save(image.name, image)
            print('worked upload')
            return HttpResponseRedirect('/staff/?email=%s' % ustaff.user.email)
        else:
            return HttpResponseRedirect('/staff/')
    else:
        messages.error(incoming, 'Login to proceed!')
        return HttpResponseRedirect('/')


def update_user_profile(incoming):
    try:
        if incoming.method == "POST":
            email = incoming.POST['email']

            first_name = incoming.POST['first_name']
            last_name = incoming.POST['last_name']
            contact = incoming.POST['contact']
            address = incoming.POST['address']
            nin = incoming.POST['nin']
            gender = incoming.POST['gender']
            staff_responsibilities = incoming.POST['staff_responsibilities']
            position = incoming.POST['position']

            user = User.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            mf = Staff.objects.get(user=user)

            Staff.objects.filter(code=mf.code).update(
                user=user,
                contact=contact,
                address=address,
                nin=nin,
                gender=gender,
                staff_responsibilities=staff_responsibilities,
                position=position,
            )
            messages.success(incoming, 'Updated User Profile Successfully')
            return HttpResponseRedirect('/staff/?email=%s' % email)
        else:
            messages.error(incoming, 'FAILED!!!')
            return HttpResponseRedirect('/')
    except Exception as p:
        print(str(p))
        messages.error(incoming, 'FAILED!!! %s' % p)
        return HttpResponseRedirect('/')


def all_staff(incoming):
    if incoming.user.is_superuser and incoming.user.is_authenticated:
        if incoming.method == 'POST':
            first_name = incoming.POST["first_name"]
            last_name = incoming.POST["last_name"]
            email = incoming.POST["email"]
            username = incoming.POST["username"]

            dept_code = incoming.POST["dept_code"]
            role_code = incoming.POST["role_code"]

            contact = incoming.POST["contact"]
            address = incoming.POST["address"]
            nin = incoming.POST["nin"]
            gender = incoming.POST["gender"]

            dob = incoming.POST["dob"]
            password = incoming.POST["password"]
            staff_responsibilities = incoming.POST["staff_responsibilities"]
            position = incoming.POST["position"]

            # Department
            department = Department.objects.get(code__contains=dept_code)
            # Role
            role = Role.objects.get(code__contains=role_code)

            # User
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            password=password,
                                            is_staff=True
                                            )

            Staff.objects.create(
                code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                user=user,
                department=department,
                role=role,
                contact=contact,
                address=address,
                nin=nin,
                gender=gender,
                dob=dob,
                staff_status='active',
                staff_responsibilities=staff_responsibilities,
                position=position

            )
            messages.success(incoming, 'You have successfully registered Staff')
            return HttpResponseRedirect("/all_staff/")
        else:
            staffs = Staff.objects.all().filter(Q(role__name__contains='STAFF') | Q(role__name__contains='FINANCE'))
            departments = Department.objects.all()
            access = Role.objects.all()
            return render(incoming, 'new/staff.html',
                          {'staffs': staffs, 'departments': departments, 'access': access})
    else:
        return HttpResponseRedirect('/')


def administrators(incoming):
    if incoming.user.is_superuser and incoming.user.is_authenticated:
        if incoming.method == 'POST':
            first_name = incoming.POST["first_name"]
            last_name = incoming.POST["last_name"]
            email = incoming.POST["email"]
            username = incoming.POST["username"]

            dept_code = incoming.POST["dept_code"]
            role_name = incoming.POST["role_name"]

            contact = incoming.POST["contact"]
            address = incoming.POST["address"]
            nin = incoming.POST["nin"]
            gender = incoming.POST["gender"]

            dob = incoming.POST["dob"]
            password = incoming.POST["password"]
            staff_responsibilities = incoming.POST["staff_responsibilities"]

            # Department
            department = Department.objects.get(code__contains=dept_code)
            # Role
            role = Role.objects.get(name__contains=role_name)

            # User
            user = User.objects.create_superuser(username=username,
                                                 first_name=first_name,
                                                 last_name=last_name,
                                                 email=email,
                                                 password=password,
                                                 is_staff=True,
                                                 is_superuser=True
                                                 )

            Staff.objects.create(
                code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                user=user,
                department=department,
                role=role,
                contact=contact,
                address=address,
                nin=nin,
                gender=gender,
                dob=dob,
                staff_status='active',
                staff_responsibilities=staff_responsibilities
            )
            messages.success(incoming, 'You have successfully registered Super User')
            return HttpResponseRedirect("/administrators/")
        else:
            admins = Staff.objects.all().filter(
                Q(role__name__contains='ADMINISTRATOR') | Q(role__name__contains='MANAGING DIRECTOR'))

            departments = Department.objects.all()
            access = Role.objects.all()
            return render(incoming, 'new/administrators.html', {'admins': admins, 'departments': departments})
    else:
        return HttpResponseRedirect('/')


def staff(incoming):
    if incoming.user.is_authenticated:
        try:
            email = incoming.GET['email']
            staff_detail = Staff.objects.get(user__email__contains=email)
            print('staff details page')
            return render(incoming, 'new/staff_detail.html', {'profile': staff_detail})
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/')
    else:
        messages.error(incoming, 'Login to Proceed')
        return HttpResponseRedirect('/')


def delete_staff(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        try:
            email = incoming.GET['email']
            # staff_detail = Staff.objects.get(user__email__contains=email)
            # Delete Staff
            Staff.objects.get(user__email__contains=email).delete()
            # Delete User
            User.objects.get(email__contains=email).delete()
            messages.success(incoming, 'User has been Deleted Successfully')
            return HttpResponseRedirect('/all_staff/')
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/all_staff/')
    else:
        messages.error(incoming, 'Login to Proceed')
        return HttpResponseRedirect('/')
