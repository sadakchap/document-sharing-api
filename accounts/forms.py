from django import forms
from django.contrib.auth import get_user_model, authenticate
from string import ascii_lowercase, digits
from random import choice

User = get_user_model()

def generate_random_username(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in range(length)])
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])
    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'autofocus':'on'}))
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password',)
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        pswd = self.cleaned_data.get('password')

        if email and pswd:
            user = authenticate(username=email, password=pswd)
            print(email, pswd)
            if not user:
                raise forms.ValidationError('This email is not registered!')
            if not user.check_password(pswd):
                raise forms.ValidationError('Incorrect Password!')
            if not user.is_active:
                raise forms.ValidationError('Not active')
            return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Sorry, email already taken!')
        return email
    
    def clean(self, *args, **kwargs):
        pwrd1 = self.cleaned_data.get('password1')
        pwrd2 = self.cleaned_data.get('password2')
        if pwrd1 and pwrd2 and pwrd1 != pwrd2:
            raise forms.ValidationError('Both passwords must match!')
        return super(UserRegisterForm, self).clean(*args, **kwargs)
    
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.username = generate_random_username()
        if commit:
            user.save()
        return user
        
