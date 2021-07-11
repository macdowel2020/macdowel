from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render


def login(incoming):
    if incoming.method == "GET":
        return render(incoming, 'authenticate/login.html', {"app": "login"})
    else:
        try:
            username = incoming.POST["username"]
            password = incoming.POST["password"]
            # if the fields are not empty
            if username != "" and password != '':
                # authenticate the user
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    # authenticate the user
                    auth.login(incoming, user)
                    print('perez worked')
                    # record action
                    # AuditTrail.objects.create(user=user, action="Logged in successfully")
                    return HttpResponseRedirect('/')
                else:
                    return render(incoming, 'authenticate/login.html',
                                  {'error': 'The user account does not exists!!'})
            else:
                return render(incoming, 'authenticate/login.html',
                              {'error': 'The user account does not exists!!'})
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/')


def logout(incoming):
    # record action
    try:
        # AuditTrail.objects.create(user=incoming.user, action="Logged out successfully")
        auth.logout(incoming)
        return HttpResponseRedirect('/')
    except Exception as p:
        print(str(p))
        # auth.logout(incoming)
        return HttpResponseRedirect('/')