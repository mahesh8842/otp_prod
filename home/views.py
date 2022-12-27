from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .helpers import send_otp_to_mobile
from django.contrib import auth
from django.contrib.auth import logout
import re
# Create your views here.

def home(request):
    return render(request,'home.html',{'user':request.user})

def login(request):
    if request.method=='POST':
        mobile=request.POST.get('mobile','')
        if validate_mobile(mobile)==None:
            return render(request,'login.html',{'class':'danger','message':'Please enter a valid mobile number!'})
        else:
            print(request.POST.get('otp'))
            user = User.objects.filter(phone_num=mobile).first()
            if user is None:
                return render(request,'login.html',{'class':'danger','message':'User invalid please register!'})
            if request.POST.get('otp')==None:
                if user.otp==None:
                    return render(request,'login.html',{'mobile':mobile,'display':True,'class':'danger','message':'Not Registered!'})
                else:
                    print(user.otp,'otp')
                    send_otp_to_mobile(mobile,int(user.otp))
                    return render(request,'login.html',{'mobile':mobile,'display':True,'class':'success','message':'Otp sent successfully!'})
            else:
                otp = request.POST.get('otp')   
                if user.otp==otp:
                    auth.login(request,user)
                    return redirect('/')
                else:
                    return render(request,'login.html',{'class':'danger','message':'Please enter a valid otp!'})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def profile(request):
    user = request.user
    user = User.objects.get(username=user)
    return render(request,'profile.html',{'user':user})

def verify(request):
    user = request.user
    otp = request.POST.get('otp')
    print(otp,user)
    try:
        user = User.objects.filter(username=user.username).first()
        if user.otp==otp:
            return render(request,'home.html',{'message':'otp verification successful!'})
        else:
            return render(request,'login_otp.html',{'mobile':'enter valid otp!'})
    except Exception as e:
        print(e)

def register(request):
    if request.method=='POST':
        print(request.POST)
        email=request.POST.get('email','')
        username=request.POST.get('username','')
        mobile=request.POST.get('mobile','')
        # print(validate_email_address(email),name,mobile)
        if validate_email_address(email)==None:
            return render(request,'register.html',{'mail':'danger','class':'danger','message':'Please enter a valid email id!','name_p':username,'mobile_p':mobile})
        if validate_mobile(mobile)==None:
            return render(request,'register.html',{'mobile':'danger','class':'danger','message':'Please enter a valid mobile number!','mail_p':email,'name_p':username})
        try:
            obj = User.objects.get(username=username)
            if obj is not None:
                return render(request,'register.html',{'class':'danger','message':'User already exists please login'})
        except Exception as e:
            user=User.objects.create(username=username,email=email,phone_num=mobile,
            otp = send_otp_to_mobile(mobile))
            print(user.otp)
            return redirect('/login')

    return render(request,'register.html')

def validate_email_address(email_address):
  
   return re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address)
#    r'^\+?1?\d{9,15}$
def validate_mobile(mobile):
    return re.search(r'^\+?1?\d{9,12}$',mobile)


@api_view(['POST'])
def send_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status':400,
            'message':'Phone number is required!!'
            })
    if data.get('password') is None:
        return Response({
            'status':400,
            'message':'password is required!!'
            })

    