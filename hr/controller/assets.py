import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Asset, Staff


def all_assets_list(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        if incoming.method == 'POST':
            try:
                categories = incoming.POST['categories']
                description = incoming.POST['description']
                number = incoming.POST['number']
                amount_sold = incoming.POST['amount_sold']
                sold_to = incoming.POST['sold_to']
                purchase_id = incoming.POST['purchase_id']
                date = incoming.POST['date']

                staff = Staff.objects.get(user__email__contains=incoming.user.email)
                Asset.objects.create(
                    code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                    added_by=staff,
                    categories=categories,
                    description=description,
                    number=number,
                    amount_sold=amount_sold,
                    sold_to=sold_to,
                    purchase_id=purchase_id,
                    date=date
                )
                messages.success(incoming, 'Asset has been successfully created')
                return HttpResponseRedirect('/all_assets_list/')
            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/all_assets_list/')
        else:
            # List view is here
            assets = Asset.objects.all().order_by('-id')
            return render(incoming, 'assets_of_company.html', {'assets': assets})
    else:
        return HttpResponseRedirect('/')


def delete_asset(incoming):
    if incoming.user.is_superuser and incoming.user.is_authenticated:
        try:
            idx = incoming.GET['id']
            Asset.objects.get(id=idx).delete()
            messages.success(incoming, 'Asset has been deleted successfully')
            return HttpResponseRedirect('/all_assets_list/')
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/all_assets_list/')
    else:
        messages.error(incoming, 'You are not allowed to perform this action')
        return HttpResponseRedirect('/')
