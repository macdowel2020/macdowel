import random
import string

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Staff, Project, Department, Role, AuditTrail


def profile(request):
    if request.user.is_authenticated:
        try:
            staff = Staff.objects.get(user=request.user)
            if request.method == "POST":

                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                email = request.POST["email"]
                username = request.POST["username"]

                project_code = request.POST["project_code"]
                dept_code = request.POST["dept_code"]
                role_code = request.POST["role_code"]

                contact = request.POST["contact"]
                address = request.POST["address"]
                nin = request.POST["nin"]
                gender = request.POST["gender"]

                dob = request.POST["dob"]
                password = request.POST["password"]
                staff_responsibilities = request.POST["staff_responsibilities"]

                if request.user.is_staff:

                    try:
                        # Get Project
                        # User
                        user = User.objects.create_user(username=username,
                                                        first_name=first_name,
                                                        last_name=last_name,
                                                        email=email,
                                                        password=password,
                                                        is_staff=True
                                                        )
                        # Project
                        project = Project.objects.get(code__contains=project_code)
                        # Department
                        department = Department.objects.get(code__contains=dept_code)
                        # Role
                        role = Role.objects.get(code__contains=role_code)

                        Staff.objects.create(
                            code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                            user=user,
                            project=project,
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
                        # record action
                        AuditTrail.objects.create(user=request.user, project=staff.project,
                                                  action="Created <a href='/staff/?email=%s' target='_blank'>%s %s's</a> staff profile" % (
                                                      email, first_name, last_name))

                        messages.success(request, 'You have successfully registered Staff')
                        return HttpResponseRedirect("/staff/")

                    except Exception as p:
                        print(str(p))
                        return HttpResponseRedirect("/")
                else:
                    messages.error(request, 'You are not allowed to perform this action')
                    return HttpResponseRedirect("/")

            else:
                try:
                    # Get details of staff
                    user = User.objects.get(email=request.GET["email"])
                    staff = Staff.objects.get(user=user)
                    trail = AuditTrail.objects.filter(user=user)
                    return render(request, "authenticate/users.html", {"profile": staff, "view": "details", "trail": trail})

                except Exception as p:
                    print(str(p))
                    # Get all staff
                    if request.user.is_superuser and request.user.is_staff:
                        staffs = Staff.objects.all().order_by('-id')
                        projects = Project.objects.all()
                        departments = Department.objects.all()
                        roles = Role.objects.all()
                    elif request.user.is_staff:
                        projects = Staff.objects.get(user=request.user)
                        staffs = Staff.objects.filter(project=projects.project).order_by('-id')
                        projects = Project.objects.all()
                        departments = Department.objects.all()
                        roles = Role.objects.all()
                    else:
                        projects = Staff.objects.get(user=request.user)
                        staffs = Staff.objects.filter(project=projects.project).order_by('-id')
                        projects = Project.objects.all()
                        departments = Department.objects.all()
                        roles = Role.objects.all()
                    return render(request, "authenticate/users.html",
                                  {"staffs": staffs, "view": "staff", "projects": projects, 'departments': departments,
                                   'roles': roles})
        except Exception as p:
            print(str(p))
            messages.error(request, 'Invalid Profile')
            return HttpResponseRedirect("/")
    else:
        messages.error(request, 'Login to Continue')
        return HttpResponseRedirect("/")


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

            user = User.objects.get(email=email)
            user.first_name=first_name
            user.last_name=last_name
            user.save()

            mf = Staff.objects.get(user=user)

            Staff.objects.filter(code=mf.code).update(
                user=user,
                contact=contact,
                address=address,
                nin=nin
            )
            messages.success(incoming, 'Updated User Profile Successfully')
            return HttpResponseRedirect('/staff/?email=%s' % email)
        else:
            messages.error(incoming, 'FAILED!!!')
            return HttpResponseRedirect('/')
    except Exception as p:
        print(str(p))
        messages.error(incoming, 'FAILED!!! %s'%p)
        return HttpResponseRedirect('/')
