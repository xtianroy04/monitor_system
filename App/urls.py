from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login', views.login, name="login"),
    path('', views.index, name="dashboard"),
    path('register', views.register_attendee, name="register"),
    path('attendee/<int:attendee_id>/', views.attendee_detail, name='attendee_detail'),
    path('attendee/sign-in/<int:attendee_id>/', views.sign_in_attendee, name='sign_in_attendee'),
    path('attendance-sheet', views.attendance_sheet, name="attendance_sheet"),
    path('logout/', views.logout, name='logout'),
]
