from django.shortcuts import render, redirect
from .forms import reg_form
from .forms import Profile_form
from .models import Profile
from Productmanagement.models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import message, send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
UserModel = get_user_model()


# Create your views here.

def registration(request) :
    form = reg_form()
    message = "Insert Information"

    if request.method == "POST" :
        form = reg_form(request.POST)
        message = "Invalid Information"

        if form.is_valid() :
            user = form.save()

            cart = Cart(user = user)
            cart.save()

            user=form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject='Activate Your Account'
            message=render_to_string('UserManagement/account.html',{
                'user':user,
                'domain': current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            send_mail=form.cleaned_data.get('email')
            email=EmailMessage(mail_subject,message, to=[send_mail])
            email.send()
            messages.success(request, 'Successfully Create Account.')
            messages.info(request, 'Activate Your Account From The Email You Provided.')

            return redirect('http://localhost:8000/accounts/login')

    context = {
        'form' : form,
        'message' : message
    }
    return render(request, 'Registration/registration.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated now, you can now login")
        return redirect('http://localhost:8000/accounts/login')
    else:
        messages.warning(request, "Activation link is invalid")
        return redirect('http://localhost:8000/registration')

@login_required
def createprofile(request) :
    form = Profile_form()

    if request.method == "POST" :
        form = Profile_form(request.POST, request.FILES)
    
    if form.is_valid() :
        profile_object = form.save(commit=False)
        profile_object.user = request.user
        profile_object.save()

        return redirect('viewprofile')

    try : 
        value = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        value = '0'

    context = {
        'form' : form,
        'value' : value,
    }

    return render(request, 'UserManagement/create_profile.html', context)


def showprofile(request) :
    try :
        profile = Profile.objects.get(user = request.user)
    except Profile.DoesNotExist:
        profile = print("Please Complete Your Profile To View")

    context = {
        'profile' : profile
    }
    return render(request, 'UserManagement/view_profile.html', context)

def email(request):
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)
        return render(request, 'UserManagement/sent_email_confirm.html', {'email': email})

    return render(request, 'UserManagement/sent_email.html', {})