from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('contact/',views.contact,name='contact'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('book_details/<id>',views.book_details,name='book_details')
]