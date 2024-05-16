from django.shortcuts import render, redirect
from fapp.forms import UserForm  #, UserProfileForm
from django.views import View #CBV

#Login libraries

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib import messages

#Mail libraries

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'fapp/index.html')

@method_decorator(login_required, name='dispatch') #Only active if logged in
class search(View):
    def get(self, request):
        return render(request, 'fapp/search.html')  

class user_logout(View):
    def log_out(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('fapp:index'))

#註冊
class register(View):
    def get(self, request):
        registered = False
        user_form = UserForm()
        # profile_form = UserProfileForm()
        return render(request, 'fapp/registration.html', 
                    {'user_form': user_form, 
                    'registered': registered})
    
    def post(self, request):

        registered = False
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid():
        # if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # profile = profile_form.save(commit=False) # don't commit to the database
            # profile.user = user #set 1 to 1 relationship

            # if 'profile_pic' in  request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']

            # profile.save()

            registered = True

        else:
            # print(user_form.errors, profile_form.errors)
            print(user_form.errors)
            
        return render(request, 'fapp/registration.html', 
                    {'user_form': user_form, 
                    'registered': registered})

    # return render(request, 'fapp/registration.html', 
    #               {'user_form': user_form, 
    #                'profile_form': profile_form,
    #                'registered': registered})

#登入函數
class user_login(View):
    def get(self, request):
        return render(request, 'fapp/index.html', {})

    def post(self, request):

        email_address = request.POST.get('email') # get username that equals the input name='email' in login page
        password = request.POST.get('password') # get password that equals the input name='password' in login page
        user = authenticate(username=email_address, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('fapp:search'))
            else:
                return render(request, 'fapp/index.html', {'error_message': 'Inactive Account'})
            
        else:
            print(user)
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(email_address,password))
            return render(request, 'fapp/index.html', {'error_message': 'Invalid Email or Password'})


#發送郵件&重設密碼
@method_decorator(login_required, name='dispatch') 
class sendmail(View):

    def get(self, request):
        return render(request, 'fapp/resetpwd.html')
    
    def post(self, request):

        if request.user.is_authenticated:

            current_site = get_current_site(request)

            #電子郵件內容模板
            email_content = render_to_string(
                "fapp/email_template.html",
                {'username': request.user.username.split('.')[0],
                 'request': request,
                 'domain': current_site.domain,
                 'uid':urlsafe_base64_encode(force_bytes(request.user.pk)),
                 'token':account_activation_token.make_token(request.user),
                 })
        
            if request.method == 'POST':

                email = EmailMessage(
                    '【EY Web Crawler】重設密碼通知',  # 電子郵件標題
                    email_content,  # 電子郵件內容
                    settings.EMAIL_HOST_USER,  # 寄件者
                    [request.user.username]  # 收件者
                )
                email.fail_silently = False
                email.send()
                messages.error(request, "驗證信已寄出，請使用新密碼登入") 

                return render(request, 'fapp/index.html', {})
            
        else:
            return HttpResponseRedirect(reverse('fapp:search'))
            # return render(request, 'fapp/index.html', {'error_message': 'Invalid User'})

#電子郵件驗證連結
class verify_email(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('fapp:reset'))
        else:
            return HttpResponse('Activation link is invalid!')

#重設密碼連頁面 待後續調整
class resetpage(View):
    def get(self, request):
        return render(request, 'fapp/mail_reset.html')
    

