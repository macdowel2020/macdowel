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

from django.conf import settings
from django.conf.urls.static import static

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

    #     PROJECT DETAILS

    path('farm_detail/', farms.p_detail, name='farm_detail'),
    path('add_farm_income/', farms.income, name='add_farm_income'),
    path('request_expenditure/', farms.request_expenditure, name='request_expenditure'),
    path('approve_request/', farms.approve_request, name='approve_request'),
    path('reject_request/', farms.reject_request, name='reject_request'),
    path('delete_expenditure/', farms.delete_expenditure, name='delete_expenditure'),
    path('update_project_photo/', farms.update_project_photo, name='update_project_photo'),
    path('farm_inventory/', farms.inventory, name='farm_inventory'),
    path('delete_inventory/', farms.delete_inventory, name='delete_inventory'),

    #     PROJECTS
    path('machines/', machinery.machines, name='machines'),
    path('farms/', farms.farms, name='farms'),

    #     LAND
    path('land/', land.land, name='land'),
    path('delete_project/', farms.delete_project, name='delete_project'),

    #     STAFF
    path('update_staff_photo/', register.update_staff_photo, name='update_staff_photo'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
