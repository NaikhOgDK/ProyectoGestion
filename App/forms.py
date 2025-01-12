from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
import re

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, error_messages={
        'required': 'Este campo es obligatorio.',
        'invalid': 'Por favor, introduce un correo electrónico válido.'
    })
    
    # Personalización de mensajes de error
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'group']

    # Validación personalizada para el campo username
    username = forms.CharField(
        max_length=150,
        error_messages={
            'required': 'Este campo es obligatorio.',
            'max_length': 'El nombre de usuario no puede tener más de 150 caracteres.',
        }
    )

    # Validación personalizada para el campo password1
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'min_length': 'La contraseña debe tener al menos 8 caracteres.',
        }
    )
    
    # Validación personalizada para el campo password2
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'invalid': 'Las contraseñas no coinciden.',
        }
    )

    # Validación para el campo email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    # Validación para password1
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        # Puedes agregar más validaciones aquí como verificar si la contraseña es demasiado simple.
        if password.isnumeric():
            raise forms.ValidationError("La contraseña no puede ser completamente numérica.")
        if re.match(r'^[a-zA-Z0-9]*$', password):
            raise forms.ValidationError("La contraseña no puede ser una palabra común. Intenta con una combinación de caracteres.")
        return password

    # Validación para el campo username
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) > 150:
            raise forms.ValidationError("El nombre de usuario no puede tener más de 150 caracteres.")
        # Puedes agregar más validaciones si es necesario
        return username

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
