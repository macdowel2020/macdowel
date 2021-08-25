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
                asset_name = incoming.POST['asset_name']
                asset_model = incoming.POST['asset_model']
                serial_number = incoming.POST['serial_number']
                cost = incoming.POST['cost']
                description = incoming.POST['description']
                date = incoming.POST['date']
                date_sold = incoming.POST['date_sold']
                location = incoming.POST['location']
                purchase_id = incoming.POST['purchase_id']
                purchase_date = incoming.POST['purchase_date']

                staff = Staff.objects.get(user__email__contains=incoming.user.email)
                Asset.objects.create(
                    code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                    asset_name=asset_name,
                    asset_model=asset_model,
                    serial_number=serial_number,
                    cost=cost,
                    description=description,
                    date=date,
                    date_sold=date_sold,
                    location=location,
                    purchase_id=purchase_id,
                    added_by=staff,
                    purchase_date=purchase_date
                )
                messages.success(incoming, 'An Asset has been successfully created')
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
