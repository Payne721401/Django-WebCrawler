from django.shortcuts import render, redirect
from django.views import View #CBV

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


#待處理
@method_decorator(login_required, name='dispatch') #Only active if logged in
class search(View):
    def get(self, request):
        return render(request, 'fapp/search.html')  