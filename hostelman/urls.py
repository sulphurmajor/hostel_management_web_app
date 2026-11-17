"""
URL configuration for hostelman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from hostel.views import (
    hostel_form_view,
    index_view,
    payments_view,
    student_form_view,
    warden_form_view,
    room_form_view,
    edit_student_view,
    delete_student_view,
    entity_delete_view,
    entity_edit_view,
    entity_manage_view,
    visitor_form_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', index_view, name="index_view"),
    path('payments/', payments_view, name='payments_view'),
    path('students/add/', student_form_view, name='student_form'),
    path('hostels/add/', hostel_form_view, name='hostel_form'),
    path('wardens/add/', warden_form_view, name='warden_form'),
    path("rooms/add/", room_form_view, name="room_form"),
    path("visitors/add/", visitor_form_view, name="visitor_form"),
    path("<str:entity>/", entity_manage_view, name="entity_manage"),
    path("<str:entity>/<int:item_id>/edit/", entity_edit_view, name="entity_edit"),
    path("<str:entity>/<int:item_id>/delete/", entity_delete_view, name="entity_delete"),
    path('students/<int:student_id>/edit/', edit_student_view, name='edit_student'),
    path('students/<int:student_id>/delete/', delete_student_view, name='delete_student'),
]
