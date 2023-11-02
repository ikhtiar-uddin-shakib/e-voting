from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from api.models import *
from .forms import RegistrationForm, Changepass, Change_pass
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# new coder code for toster
def account_login(request):
    user = request.user
    if user.is_authenticated:
       return redirect('userProfile')
    elif request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)        
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('userDashboard')
        else:
            messages.error(request, "Invalid details")
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html')


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect('login') 


# user register with email varification
def account_register(request):
    user = request.user
    if user.is_authenticated:
       return redirect('userProfile')
    
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate Your Account"
            message = render_to_string('account/varify_email.html',{
                'user': request.user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                
            })
            send_mail = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[send_mail])
            email.send()
            messages.success(request, 'Account Created Successfully')
            messages.info(request, 'Activate your account from your provided email')
            # login(request, user)
            return redirect('login') 
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


# Account acivation function from email here
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated. You Can login now')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')



# change passsword without old password
def change_pass(request):
    # if request.user.is_authenticated:
    form = Change_pass(user=request.user, data=request.POST) 
    if request.method == 'POST':        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # password update kora hocce
            # messages.success('Your Password updated successfully')
            return redirect('userDashboard')
        
        else:
            form = Change_pass(user = request.user)
    return render(request, 'account/pass_change.html', {'form':form})
    # return redirect('change_pass')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('account/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'account/forgotPassword.html' )


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'account/resetPassword.html')



def profile(request):
    return render(request,'account/footer/team.html')

def aboutus(request):
    return render(request,'account/footer/about.html')
def how_to_use(request):
    return render(request, 'account/footer/how_to_use.html')