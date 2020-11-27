from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('profile',views.profile,name='myprofile'),
    path('',views.homepage,name='homepage'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('signup',views.signup,name='signup'),
    path('save',views.save,name='save'),
    path('delete',views.delete,name='delete'),
    path('edit',views.edit,name='edit'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]