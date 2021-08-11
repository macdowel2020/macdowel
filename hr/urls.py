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
from hr.controller import home, authenticate, register, departments, projects, \
    project_categories, filter_projects

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home.dashboard, name='dashboard'),
    #     Authenticate
    path('login/', authenticate.login, name='login'),
    path('logout/', authenticate.logout, name='logout'),

    #     STAFF
    path('update_staff_photo/', register.update_staff_photo, name='update_staff_photo'),
    path('update_user_profile/', register.update_user_profile, name='update_user_profile'),
    path('staff/', register.staff, name='staff'), # Staff Details

    #     =========== NEW =========
    path('project_categories/', project_categories.project_categories, name='project_categories'),
    path('delete_location/', project_categories.delete_location, name='delete_location'),
    path('all_projects/', projects.all_projects, name='all_projects'),
    path('project_detail/', projects.project_detail, name='project_detail'),

    #     STAFF
    path('all_staff/', register.all_staff, name='all_staff'),
    path('administrators/', register.administrators, name='administrators'),
    path('departments/', departments.dept, name='departments'),
    path('roles/', departments.role, name='roles'),
    path('delete_role/', departments.delete_role, name='delete_role'),
    path('delete_department/', departments.delete_department, name='delete_department'),
    #     Filters
    path('filter_projects/', filter_projects.filter_projects, name='filter_projects'),
    #     Project
    path('update_project_photo/', projects.update_project_photo, name='update_project_photo'),
    path('add_farm_income/', projects.income, name='add_farm_income'),
    path('request_expenditure/', projects.request_expenditure, name='request_expenditure'),
    path('approve_request/', projects.approve_request, name='approve_request'),
    path('reject_request/', projects.reject_request, name='reject_request'),
    path('delete_expenditure/', projects.delete_expenditure, name='delete_expenditure'),
    path('farm_inventory/', projects.inventory, name='farm_inventory'),
    path('delete_inventory/', projects.delete_inventory, name='delete_inventory'),
    path('delete_project/', projects.delete_project, name='delete_project'),
    path('edit_and_request/', projects.edit_and_request, name='edit_and_request'),
    path('add_staff_to_project/', projects.add_staff_to_project, name='add_staff_to_project'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
