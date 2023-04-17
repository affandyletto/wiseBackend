from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.http import HttpResponse

from functools import wraps

PERMISSION_TYPES = {
    "SuperAdmin" : lambda request: request.user.profile.isSuperAdmin,
    "CompanyAdmin" : lambda request: request.user.profile.isCompanyAdmin,
    "AccountManager":lambda request:request.user.profile.isAccountManager,
    "Technician":lambda request:request.user.profile.isTechnician,
}

def requirePermissionsViews(*args):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            if any(permission(request) for permission in permissions.values()):
                return function(request, *args, **kwargs)
            messages.warning(request, "You do not have the valid permissions to view that page. Required: {}".format(" or ".join(permissions)))
            return HttpResponse("<script>window.history.back();</script>")
        return wrapper

    permissions = {}
    for x in args:
        try:
            permissions[x] = PERMISSION_TYPES[x]
        except:
            raise Exception("{} is not a valid permission type. Must be one of the following: {}".format(x, PERMISSION_TYPES.keys()))     

    required_permissions_str = " or ".join(permissions.keys()) 

    return decorator