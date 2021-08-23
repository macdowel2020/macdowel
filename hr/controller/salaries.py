import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Salary, Staff


def salary_payments(incoming):
    if incoming.user.is_authenticated:
        salaries = Salary.objects.all().order_by('-id')
        return render(incoming, 'salaries.html', {'salaries': salaries})
    else:
        messages.error(incoming, 'Login to Proceed')
        return HttpResponseRedirect('/')


def load_add_salary_page(incoming):
    if incoming.user.is_authenticated:
        staff = Staff.objects.all()
        return render(incoming, 'add_salary.html', {'staff': staff})
    else:
        messages.error(incoming, 'Login to Proceed')
        return HttpResponseRedirect('/')


def add_salary(incoming):
    if incoming.user.is_authenticated:
        if incoming.method == 'POST':
            try:
                # code =
                category = incoming.POST['category']
                expected_amount = incoming.POST['expected_amount']
                amount_paid = incoming.POST['amount_paid']
                description = incoming.POST['description']
                paid_on = incoming.POST['paid_on']
                xcode = incoming.POST['payment_to']

                payment_to = Staff.objects.get(code=xcode)

                # Calculate Balance
                balance = int(expected_amount) - int(amount_paid)

                Salary.objects.create(
                    code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                    payment_to=payment_to,
                    category=category,
                    expected_amount=expected_amount,
                    amount_paid=amount_paid,
                    description=description,
                    status='PAID',
                    paid_on=paid_on,
                    balance=balance
                )
                messages.success(incoming, 'Successfully recorded Transaction')
                return HttpResponseRedirect('/salary_payments/')
            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/salary_payments/')
        else:
            return HttpResponseRedirect('/salary_payments/')
    else:
        messages.error(incoming, 'Login to Proceed')
        return HttpResponseRedirect('/')


def delete_salary(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        try:
            idx = incoming.GET['id']
            Salary.objects.get(id=idx).delete()
            messages.success(incoming, 'Salary Transaction has been deleted Successfully')
            return HttpResponseRedirect('/salary_payments/')
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/salary_payments/')
    else:
        messages.error(incoming, 'Login to Proceed')
        return HttpResponseRedirect('/')


def edit_salary(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        if incoming.method == 'POST':
            try:
                category = incoming.POST['category']
                expected_amount = incoming.POST['expected_amount']
                amount_paid = incoming.POST['amount_paid']
                description = incoming.POST['description']

                idx = incoming.POST['id']
                salary_x = Salary.objects.get(id=idx)

                # Calculate Balance
                balance = 0
                balance = int(expected_amount) - int(amount_paid)

                if int(balance) == 0:
                    status = 'FULLY PAID'
                else:
                    status = 'PARTIALLY PAID'

                Salary.objects.filter(id=salary_x.id).update(
                    category=category,
                    expected_amount=expected_amount,
                    amount_paid=amount_paid,
                    description=description,
                    status=status,
                    balance=balance,
                )
                messages.success(incoming, 'Salary Transaction has been Updated Successfully')
                return HttpResponseRedirect('/salary_payments/')
            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/salary_payments/')
        else:
            try:
                idx = incoming.GET['id']
                salary_detail = Salary.objects.get(id=idx)
                user_n = salary_detail.payment_to
                staff = Staff.objects.get(user__username=user_n)
                return render(incoming, 'edit_salary.html', {'salary_detail': salary_detail, 'staff': staff})
            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/salary_payments/')

    messages.error(incoming, 'Login to Proceed')
    return HttpResponseRedirect('/')
