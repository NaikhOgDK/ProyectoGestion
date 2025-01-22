from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
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


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = [
            'Mantencion_Preventiva', 'fecha_vencimiento_mantencion',
            'Revision_Tecnica', 'fecha_vencimiento_revision',
            'Permiso_Circulacion', 'fecha_vencimiento_permiso',
            'SOAP', 'fecha_vencimiento_soap',
            'Padron', 'fecha_vencimiento_padron',
            'descripcion'
        ]

    Mantencion_Preventiva = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    fecha_vencimiento_mantencion = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    Revision_Tecnica = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    fecha_vencimiento_revision = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    Permiso_Circulacion = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    fecha_vencimiento_permiso = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    SOAP = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    fecha_vencimiento_soap = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    Padron = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    fecha_vencimiento_padron = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción adicional'}),
        required=False
    )


class MantenimientoForm(forms.ModelForm):
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(),
        empty_label="Selecciona un vehículo",
        widget=forms.Select(attrs={'class': 'form-control vehiculo-select'})
    )
    kilometraje_mtto = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kilometraje'})
    )
    fecha_mtto = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    servicio_realizado = forms.ChoiceField(
        choices=Mantenimiento.SERVICIOS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    respaldo_mtto = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    proximo_mantenimiento_km = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kilometraje próximo mantenimiento'})
    )
    proximo_servicio = forms.ChoiceField(
        choices=Mantenimiento.PROXIMO_SERVICIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Mantenimiento
        fields = ['vehiculo', 'kilometraje_mtto', 'fecha_mtto', 'servicio_realizado', 'respaldo_mtto', 'proximo_mantenimiento_km', 'proximo_servicio']

class HallazgoForm(forms.ModelForm):
    class Meta:
        model = Hallazgo
        fields = [
            'hallazgo', 'vehiculo', 'posicion_neumatico', 'fecha_inspeccion', 'tipo_hallazgo',
            'nivel_riesgo', 'responsable', 'grupo', 'evidencia','documento_cierre',
        ]
        widgets = {
            'fecha_inspeccion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hallazgo': forms.TextInput(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'posicion_neumatico': forms.Select(attrs={'class': 'form-control'}),
            'tipo_hallazgo': forms.Select(attrs={'class': 'form-control'}),
            'nivel_riesgo': forms.Select(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'evidencia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'documento_cierre': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class HallazgoCierreForm(forms.ModelForm):
    class Meta:
        model = Hallazgo
        fields = ['estado_cierre', 'descripcion_cierre', 'evidencia_cierre']
        widgets = {
            'estado_cierre': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_cierre': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'evidencia_cierre': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ComunicacionForm(forms.ModelForm):
    class Meta:
        model = ComunicacionHallazgo
        fields = ["mensaje", "evidencia_adicional"]
        widgets = {
            "mensaje": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Escribe tu mensaje..."}),
            "evidencia_adicional": forms.ClearableFileInput(attrs={"class": "form-control", "id": "Padron"}),
        }

class AsignacionVehiculoForm(forms.ModelForm):
    class Meta:
        model = Asignacion_taller
        fields = ['patente', 'taller', 'motivo']
        widgets = {
            'fecha_retiro': forms.DateInput(attrs={'type': 'date'}),  # Campo de fecha con selector
        }
        labels = {
            'patente': 'Vehículo',
            'taller': 'Taller',
            'motivo': 'Motivo',
        }

class RespuestaAsignacionForm(forms.ModelForm):
    class Meta:
        model = RespuestaAsignacion_taller
        fields = ['estado', 'comentario_rechazo', 'fecha_retiro', 'comentario']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),  # Menú desplegable estilizado
            'comentario_rechazo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Explique el motivo del rechazo si aplica'}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese el comentario si la asignación es aceptada'}),
            'fecha_retiro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
        labels = {
            'estado': 'Estado de la Respuesta',
            'comentario_rechazo': 'Motivo del Rechazo',
            'fecha_retiro': 'Fecha de Retiro',
            'comentario': 'Comentario de Aceptación',
        }

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        comentario_rechazo = cleaned_data.get('comentario_rechazo')
        fecha_retiro = cleaned_data.get('fecha_retiro')
        comentario = cleaned_data.get('comentario')

        if estado == 'Rechazada' and not comentario_rechazo:
            raise forms.ValidationError("Debe proporcionar un motivo si rechaza la asignación.")
        
        if estado == 'Aceptada':
            if not fecha_retiro:
                raise forms.ValidationError("Debe proporcionar una fecha de retiro cuando la asignación es aceptada.")
            if not comentario:
                raise forms.ValidationError("Debe proporcionar un comentario cuando la asignación es aceptada.")
        
        return cleaned_data