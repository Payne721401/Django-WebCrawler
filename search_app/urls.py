from django.urls import path
from fapp import views

#Tamplate Tagging

app_name = 'search_app'

urlpatterns = [
    path('search/', views.search.as_view(), name='search') ,    
    

]