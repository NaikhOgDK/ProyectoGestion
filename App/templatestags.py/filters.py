from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='is_vigente')
def is_vigente(value):
    today = datetime.now().date()
    if value:
        # Compara la fecha con la fecha actual
        if value >= today:
            if (value - today).days <= 30:  # Por vencer en los próximos 30 días
                return 'badge-warning'
            return 'badge-success'  # Fecha vigente
        else:
            return 'badge-danger'  # Fecha vencida
    return 'badge-secondary'  # Para fechas vacías o inválidas
