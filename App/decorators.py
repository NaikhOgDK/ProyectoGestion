from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def role_required(allowed_roles):
    """
    Decorador para verificar si el usuario tiene uno de los roles permitidos.
    :param allowed_roles: Una lista de nombres de roles permitidos.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Verificamos el rol del usuario
            user_role = request.user.role.name if request.user.role else None

            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Redirige a la vista de error personalizada
                return redirect('permission_denied')  # El nombre de la vista personalizada
        return _wrapped_view
    return decorator
