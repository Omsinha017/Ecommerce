from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import EmailActivation, GuestEmail
from django.utils.safestring import mark_safe
from django.urls import reverse
from .signals import user_logged_in

User = get_user_model()

class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            msg = """ This email does not exists, Would you like to <a href="{link}">register ?</a>
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name','email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    class Meta:
        model = User
        fields = ['full_name']


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name','email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Password"}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/email activation
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                # not active check email activation
                link = reverse("account:resend-activtion")
                reconfirm_msg = """<a href='{resend_link}'>Resend Confirmation Email</a>
                """.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please Your check your Email to confirm your account." + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed" + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This User is Inactive")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid Credentials")
        login(request,user)
        self.user = user 
        user_logged_in.send(user.__class__, instance=user, request=request)
        try:
            del request.session['guest_email_id']
        except:
            pass
        return data


class RegisterForm(forms.ModelForm):
  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name','email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False   # send confirmation Email
        if commit: 
            user.save()
        return user


class GuestForm(forms.ModelForm):
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super(GuestForm, self).save(commit=False)
        if commit: 
            obj.save()
            request = self.request
            request.session["guest_email_id"] = obj.id
        return obj
