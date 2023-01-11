from django.http import HttpResponsePermanentRedirect

from common.logging import logit_class_method


class WwwRedirectMiddleware:
    """Redirects `www.welel-noted.site` to `welel-noted.site`.

    Add tests:
    https://adamj.eu/tech/2020/03/02/how-to-make-django-redirect-www-to-your-bare-domain/
    """

    def __init__(self, get_response):
        self.get_response = get_response

    @logit_class_method
    def __call__(self, request):
        host = request.get_host().partition(":")[0]
        if host == "www.welel-noted.site":
            return HttpResponsePermanentRedirect(
                "https://welel-noted.site" + request.path
            )
        else:
            return self.get_response(request)
