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
                    messages.success(incoming, 'Welcome, we are glad to have you back!')
                    return HttpResponseRedirect('/')
                else:
                    messages.error(incoming, 'Login Failed Try Again')
                    return render(incoming, 'authenticate/login.html',
                                  {'error': 'The user account does not exists!!'})
            else:
                messages.error(incoming, 'Login Failed Try Again')
                return render(incoming, 'authenticate/login.html',
                              {'error': 'The user account does not exists!!'})
        except Exception as p:
            print(str(p))
            messages.error(incoming, 'Login Failed Try Again')
            return HttpResponseRedirect('/')


def logout(incoming):
    # record action
    try:
        # AuditTrail.objects.create(user=incoming.user, action="Logged out successfully")
        auth.logout(incoming)
        messages.success(incoming, 'You are now Logged out!')
        return HttpResponseRedirect('/')
    except Exception as p:
        print(str(p))
        # auth.logout(incoming)
        return HttpResponseRedirect('/')