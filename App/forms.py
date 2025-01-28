from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
import re

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        label="Correo electrónico"
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Selecciona un rol",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Rol"
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Selecciona un grupo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Grupo",
        required=False  # Inicialmente no obligatorio
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'group']
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirma tu contraseña',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''  # Elimina el texto de ayuda
            field.error_messages = {
                'required': f'El campo {field.label} es obligatorio.',
                'invalid': f'Introduce un valor válido para {field.label}.'
            }
        # Ajusta los placeholders para mayor claridad
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirma tu contraseña'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        group = cleaned_data.get('group')

        # Lista de roles que no requieren grupo
        roles_sin_grupo = ['Administrador', 'Visualizador']

        if role and role.name not in roles_sin_grupo and not group:
            raise forms.ValidationError({
                'group': 'El grupo es obligatorio para este rol.'
            })

        return cleaned_data

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        }),
        label="Nombre de usuario"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label="Contraseña"
    )


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

class UnidadAceptadaForm(forms.ModelForm):
    class Meta:
        model = UnidadAceptada
        fields = ['estado','fecha_inicio', 'fecha_termino', 'kilometraje', 'registro', 'costo_total']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
            'registro': forms.ClearableFileInput(attrs={'multiple': False}),
        }

class HallazgoForm(forms.ModelForm):
    # Usar el widget de tipo 'date' sin especificar el formato
    fecha_inspeccion = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})  # Usar el widget de tipo "date" en HTML
    )

    class Meta:
        model = HallazgoEmpresa
        fields = ['hallazgo', 'vehiculo', 'posicion_neumatico', 'fecha_inspeccion', 'tipo_hallazgo', 'nivel_riesgo', 'responsable', 'grupo', 'evidencia']

class CierreForm(forms.ModelForm):
    class Meta:
        model = Cierre
        fields = ['responsable_cierre', 'descripcion_cierre', 'evidencia_cierre', 'documento_cierre']

        widgets = {
            'responsable_cierre': forms.Select(),
            'descripcion_cierre': forms.Textarea(attrs={'rows': 3}),
        }