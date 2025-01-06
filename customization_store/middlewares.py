from django.shortcuts import redirect
from django.urls import reverse
from .models import GlobalSettings

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            settings = GlobalSettings.objects.first()
            if settings and settings.site_under_maintenance:
                # Permite acesso apenas para admins autenticados
                if not request.user.is_authenticated or not request.user.is_staff:
                    if request.path != reverse('maintenance'):
                        return redirect('maintenance')
        except GlobalSettings.DoesNotExist:
            pass

        return self.get_response(request)
