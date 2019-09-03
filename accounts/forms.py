from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

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