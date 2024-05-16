from django.urls import path
from fapp import views

#Tamplate Tagging

app_name = 'fapp'

urlpatterns = [
    path('search/', views.search.as_view(), name='search') ,    #domain_name/fapp/search
    path('register/',views.register.as_view(),name='register'),
    path("user_login/", views.user_login.as_view(), name='user_login') , 
    path('user_logout/', views.user_logout.as_view, name='user_logout'),
    path('verifymail/', views.sendmail.as_view(), name="sendmail"),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email.as_view(), name='verify-email-confirm'),
    path('resetpwd/', views.resetpage.as_view(), name='reset'),

]