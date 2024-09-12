from django.shortcuts import render , redirect
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from users.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout

from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.core.cache import cache
import random
from users.models import *
# from django.utils.crypto import get_random_string
# from django.contrib.auth.hashers import make_password



def registration(request):
    UFDO=UserForm()
    PFDO=ProfileForm()
    d={'UFDO':UFDO ,'PFDO':PFDO}
    
    if request.method=='POST' and request.FILES:
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST, request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            #user
            MFUFDO=NMUFDO.save(commit=False)
            password=NMUFDO.cleaned_data['password']
            MFUFDO.set_password(password)
            MFUFDO.save()
            #profile
            MFPFDO=NMPFDO.save(commit=False)
            MFPFDO.username=MFUFDO
            MFPFDO.save()

            #send mail-----
            send_mail('registration',
                      'Thank you for registering with us.',
                      'baisalidas17910@gmail.com',
                      [MFUFDO.email],
                      fail_silently=False
                      )
            return HttpResponse('Successfully registered')
        else:
            return HttpResponse('Not Valid')
     
    return render(request,'registration.html',d)

#login -----
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:           
            """
            check
            if it is active user then it is authorized or else invalid credentials.
            AUO : User object
            """
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'userLogin.html')
print("Profile model:", Profile.__name__)
print("Profile model class:", Profile.__class__.__name__)

#user logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

#user details display
@login_required
def display_uDetails(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_data.html',d)

#change password

@login_required
def change_password(request):
    # user = request.user
    
    username = request.session.get('username')
    UO = User.objects.get(username=username)
        
    if request.method=='POST':
            cp=request.POST['cp']  # cp: change password
            otp_entered = request.POST['otp']  # Fetch the entered OTP

            # Retrieve the OTP stored in the cache
            otp_stored = cache.get(f'{username}_otp')
        
            if otp_stored and str(otp_stored) == otp_entered:
                UO.set_password(cp)
                UO.save()
                #clear OTP from cache
                cache.delete(f'{username}_otp')
                return HttpResponse('password is changed')
            else:
                return HttpResponse('Invalid OTP')
    #GENERATE OTP
    otp=random.randint(100000,999999)
    cache.set(f'{UO.username}_otp',otp,timeout=300)
    send_mail(
                'Reset Password OTP',
                f'Your OTP is {otp}',
                'from@example.com',
                [UO.email],
                fail_silently=False,
            )
    request.session['username']=username    
    return render(request,'change_password.html')

#reset password

def reset_pw(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        LUO = User.objects.filter(username=username)
        if LUO.exists():
            UO = LUO.first()
            
            otp = random.randint(100000, 999999)
            cache.set(f'{username}_otp', otp, timeout=300)
            
            send_mail(
                'Reset Password OTP',
                f'Your OTP is {otp}',
                'from@example.com',
                [UO.email],
                fail_silently=False,
            )
            request.session['username'] = username
            return HttpResponseRedirect(reverse('verify_otp'))
        else:
            return HttpResponse('User not found')
    return render(request, 'reset_pw.html')

    # if request.method=='POST':
    #     un=request.POST['un']
    #     pw=request.POST['pw']

    #     LUO=User.objects.filter(username=un)

    #     if LUO:
    #         UO=LUO[0]
    #         UO.set_password(pw)
    #         UO.save()
    #         return HttpResponse('password reset is done')
    #     else:
    #         return HttpResponse('user is not present in my DB')
    # return render(request,'reset_password.html')

def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        username = request.session.get('username')
        
        if not username:
            return HttpResponse('Session expired. Please try again.')
        
        otp_stored = cache.get(f'{username}_otp')

        if otp_stored and str(otp_stored) == otp_entered:
            return HttpResponseRedirect(reverse('set_new_password'))
        else:
            return HttpResponse('Invalid OTP')
    return render(request, 'verify_otp.html')


def set_new_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        username = request.session.get('username')

        if new_password and confirm_password and new_password == confirm_password:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return HttpResponse('Password reset successful')
        else:
            return HttpResponse('Passwords do not match')
    return render(request, 'set_new_password.html')