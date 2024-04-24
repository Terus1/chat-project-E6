from django.utils.deprecation import deprecated
from django.utils.translation import ugettext as _
from rest_framework.settings import api_settings
from corsheaders.defaults import CorsMiddleware


@deprecated(
    _('CORS headers are now configured in ``corsheaders`` middleware.'),
    removed_in='3.0',
)
def get_allow_origins(origin):
    """Return a list of origins that are allowed."""
    return origin


class AllowAnyOrigin(object):
    def __init__(self):
        pass

    def __call__(self, request):
        return True


class OriginValidator(object):
    def __init__(self):
        self.origins = get_allow_origins(api_settings.ALLOWED_HOSTS)

    def __call__(self, request):
        if request.method == 'OPTIONS':
            return self.origins
        return AllowAnyOrigin()


class CorsConfig(object):
    def __init__(self):
        self.origin_validator = OriginValidator()
        self.allow_credentials = api_settings.ALLOW_CREDENTIALS
        self.expose_headers = api_settings.EXPOSE_HEADERS

    def __call__(self, request):
        if request.method == 'OPTIONS':
            response = {}
            if not self.allow_credentials:
                response['Access-Control-Allow-Credentials'] = 'false'
            response['Access-Control-Allow-Origin'] = ', '.join(self.origin_validator(request))
            response['Access-Control-Max-Age'] = '86400'
            response['Content-Type'] = 'application/json'
            return response
        return None


class CorsMiddleware(CorsMiddleware):
    def __init__(self):
        super().__init__()
        self.config = CorsConfig()