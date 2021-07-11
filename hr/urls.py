"""LOANSYSTEM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from hr.controller import home, authenticate, register, departments, projects, farms, machinery, land

urlpatterns = [
    path('', home.dashboard, name='dashboard'),
    #     Authenticate
    path('login/', authenticate.login, name='login'),
    path('logout/', authenticate.logout, name='logout'),
    path('staff/', register.profile, name='staff'),
    path('departments/', departments.dept, name='departments'),
    path('roles/', departments.role, name='roles'),
    path('staff_projects/', projects.staff_projects, name='staff_projects'),
    path('project_detail/', projects.projectDtetail, name='project_detail'),

    #     FARMS
    path('farms/', farms.farms, name='farms'),
    path('farm_detail/', farms.farm_detail, name='farm_detail'),
    path('add_farm_income/', farms.farm_income, name='add_farm_income'),
    path('request_expenditure/', farms.request_expenditure, name='request_expenditure'),
    path('approve_request/', farms.approve_request, name='approve_request'),
    path('reject_request/', farms.reject_request, name='reject_request'),
    path('delete_expenditure/', farms.delete_expenditure, name='delete_expenditure'),

    #     MACHINERY
    path('machines/', machinery.machines, name='machines'),

    #     LAND
    path('land/', land.land, name='land'),

]
