from django.shortcuts import redirect
from functools import wraps


# FUNCTION-BASED VIEW DECORATOR
def role_required(allowed_roles=[]):
    """
    Restrict access to users whose EmployeeProfile.role
    matches one of the roles in allowed_roles.
    Example:
        @role_required(["admin"])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Ensure user is logged in and has a profile
            if request.user.is_authenticated and hasattr(request.user, "employeeprofile"):
                role = request.user.employeeprofile.role
                #  allow access if role matches
                if role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            #  otherwise redirect to unauthorized page
            return redirect("unauthorized")
        return _wrapped_view
    return decorator


# CLASS-BASED VIEW MIXIN

class RoleRequiredMixin:
    """
    Mixin to restrict access to class-based views based on user role.
    Example:
        class MyView(RoleRequiredMixin, CreateView):
            allowed_roles = ["admin"]
    """
    allowed_roles = []  # list of allowed roles

    def dispatch(self, request, *args, **kwargs):
        # Check if user is logged in and has a related profile
        if request.user.is_authenticated and hasattr(request.user, "employeeprofile"):
            role = request.user.employeeprofile.role
            #  allow if the user's role is permitted
            if role in self.allowed_roles:
                return super().dispatch(request, *args, **kwargs)

        #  otherwise redirect to unauthorized
        return redirect("unauthorized")
