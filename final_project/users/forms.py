from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth import get_user_model

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text="Insert a valid e-mail address", required=True)  
    class Meta:
        model = get_user_model()
        fields =['first_name', 'last_name', 'username', 'email', 'password1', 'password2',]
        
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email'] 
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    def __innit__(self, *args, **kwargs):
        super(UserLoginForm, self).__innit__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Username or Email.'}),
        label="Username or Email*")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Password'}))
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
       model = get_user_model()
       fields = [
           'first_name',
           'last_name',
           'email',
           'description',
       ]
       
class SetPasswordForm(SetPasswordForm):
    class Meta:
       model = get_user_model()
       fields = [
           'new_passwrod1',
           'new_passwrod2',
       ]