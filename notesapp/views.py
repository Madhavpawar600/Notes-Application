from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import auth,messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import Notes
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.serializers import serialize
import json
# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        context={}
        note=Notes.objects.filter(user=request.user)
        note=reversed(note)
        context['notes']=note
        return render(request,'mainpage.html',context)
    else:
        return render(request,'index.html')

def loadNotes(request):
    notedict = Notes.objects.filter(user=request.user)
    notedictSerial = json.loads(serialize('json', notedict))
    result=''
    for i in range( len(notedictSerial)-1,-1,-1):
        result += "<div class='delete'><button class='btn btn-danger btn-lg'> Delete</button></div><div class='notes' id="+str(notedictSerial[i]['pk'])  +" ><div class='text' id='notestext'>"+ notedictSerial[i]['fields']['textnote'] +"</div><div class='timetext' id='notestime'>"+ str( notedictSerial[i]['fields']['time'] )+ "</div></div>"
    return result
@login_required
def edit(request):
    if request.method == 'POST':
        text = request.POST['textdata']
        id=request.POST['pk']
        note = Notes.objects.filter(id=int(id)).update(textnote=text,time=datetime.now())
        result = loadNotes(request)
    return HttpResponse(result)

@login_required
def delete(request):
    if request.method=='POST':
        pk=request.POST['id']
        note=Notes.objects.filter(id=int(pk))
        note.delete()
        result=loadNotes(request)
        return HttpResponse(result)
@login_required
def save(request):
    if request.method=='POST':
        text=request.POST['textdata']
        user=request.user
        note=Notes(user=user,textnote=text,time=datetime.now())
        note.save()
        result=loadNotes(request)
    return HttpResponse(result)


@login_required
def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')

def login(request):
    if request.method=='POST':
        print(request.POST)
        if len(request.POST['loginusername'])==0:
            return HttpResponse('<div class="alert alert-danger"><strong>Please Enter Username</strong></div>')
        if len(request.POST['loginpassword'])==0:
            return HttpResponse('<div class="alert alert-danger"><strong>Please Enter Password</strong></div>')
        try:
            uname=request.POST['loginusername']
            pwd=request.POST['loginpassword']
            user=auth.authenticate(username=uname,password=pwd)
            if user is not None:
                auth.login(request,user)
                return redirect(homepage)
            else:
                return HttpResponse('<div class="alert alert-danger"><strong>Invalid Login Credentials</strong></div>')
        except:
            return HttpResponse('<div class="alert alert-danger"><strong></strong></div>')
    return HttpResponse('login ho gya hai')

def signup(request):
    if request.method=='POST':
        print(request.POST)
        if len(request.POST['username'])==0:
            return HttpResponse('<div class="alert alert-danger"><strong>Please Enter Username</strong></div>')
        if len(request.POST['email'])==0:
            return HttpResponse('<div class="alert alert-danger"><strong>Please Enter Email</strong></div>')
        if len(request.POST['password'])==0:
            return HttpResponse('<div class="alert alert-danger"><strong>Please Enter Password</strong></div>')
        if len(request.POST['password2'])==0:
            return HttpResponse('<div class="alert alert-danger"><strong>Please Enter Confirm Password</strong></div>')

        if request.POST['password']==request.POST['password2']:
            try:
                user=User.objects.get(username=request.POST['username'])
                return HttpResponse('<div class="alert alert-danger"><strong>Username Already Exists</strong></div>')
            except User.DoesNotExist:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
                user.is_active=False
                user.save()
                subject='Activate your account.'
                message=render_to_string('activeemail.html',{
                    'user':user,'domain':get_current_site(request).domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                print(message)
                return HttpResponse(message)
                to_email=user.email
                email=EmailMessage(subject,message,to=[to_email])
                email.send()
                return HttpResponse('<div class="alert alert-success"><strong>Register Successfully</strong> Please confirm your email.</div>')
        else:
            return HttpResponse('<div class="alert alert-danger"><strong>Passwords don\'t match!</strong></div>')
    return HttpResponse('SignUp')

def activate(request,uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=get_user_model()._default_manager().get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Invalid Registration Token')

@login_required
def logout(request):
    auth.logout(request)
    return redirect(homepage)
