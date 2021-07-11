from django.http import HttpResponseRedirect
from django.shortcuts import render


def dashboard(incoming):
    if incoming.user.is_authenticated:
        return render(incoming, 'dashboard.html')
    else:
        return HttpResponseRedirect('/login/')