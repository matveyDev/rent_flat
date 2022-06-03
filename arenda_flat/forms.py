from allauth.account.forms import SignupForm, LoginForm
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django import forms


class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        del self.fields['password1'].widget.attrs['placeholder']
        del self.fields['password2'].widget.attrs['placeholder']


    first_name = forms.CharField(label='Имя', max_length=25, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=25, required=True)
    email = forms.EmailField(label='E-mail', required=True)
    password1 = forms.CharField(label='Пароль', max_length=100, required=True)
    password2 = forms.CharField(label='Пароль(ещё раз)', max_length=100, required=True)
    phone = forms.CharField(
        label='Телефон', validators=[RegexValidator(regex='^\1?\d{9,11}$')],
        max_length=11, required=False
    )

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        new_token = Token.objects.create(user=user)
        return user

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user
    

class MyCustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        del self.fields['login'].widget.attrs['placeholder']
        del self.fields['password'].widget.attrs['placeholder']