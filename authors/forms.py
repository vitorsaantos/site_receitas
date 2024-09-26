import re

from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()
    
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(('Password must have at least one uppercase letter, '
             'one lowercase letter and one number. '
             'The length should be at least 8 characters '),
        
        code='Invalide'
        )
    
    

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Vitor')
        add_placeholder(self.fields['last_name'], 'Ex.: Santoos')
        add_attr(self.fields['username'], 'css', 'a-css-class')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required':'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. '
             'The length should be at least 8 characters '
        ),
        validators=[strong_password],
        label='password'
    )
    
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='password2',
    )

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username',
            'email',
            'password',
            ]
        
        label = {
            'username':'Username',
            'first_name':'First name',
            'last_name':'Last name',
            'email':'E-mail',
        }

        help_texts = {
            'email':'The e-mail must be valid.',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empety',
            }
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_equal_error = ValidationError(
                'Password and Password2 must be equal',
                code='invalid')
            
            raise ValidationError({
                'password': password_equal_error,
                'password2': [
                    password_equal_error,
                ]
            })