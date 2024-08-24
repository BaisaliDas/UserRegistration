from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from users.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout

from django.urls import reverse

from django.contrib.auth.decorators import login_required


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
