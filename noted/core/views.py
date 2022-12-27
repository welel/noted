from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from common.logging import logit_view


@logit_view
def handler400(request, *args, **kwargs):
    return render(
        request,
        "error.html",
        {
            "title": _("Bad Request"),
            "status_code": 400,
            "message": _("Do not repeat this request without modification."),
        },
        status=400,
    )


@logit_view
def handler403(request, *args, **kwargs):
    return render(
        request,
        "error.html",
        {
            "title": _("Forbidden"),
            "status_code": 403,
            "message": _("Access denied."),
        },
        status=403,
    )


@logit_view
def handler404(request, *args, **kwargs):
    return render(
        request,
        "error.html",
        {
            "title": _("Page Not Found"),
            "status_code": 404,
            "message": _("We couldn't find this page."),
        },
        status=404,
    )


@logit_view
def handler500(request, *args, **kwargs):
    return render(
        request,
        "error.html",
        {
            "title": _("Internal Server Error"),
            "status_code": 500,
            "message": _("Internal Server Error. Try update the page later."),
        },
        status=500,
    )
