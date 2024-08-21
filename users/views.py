from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from users.forms import *
from django.core.mail import send_mail

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