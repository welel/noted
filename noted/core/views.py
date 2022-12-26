from django.shortcuts import render

from common.logging import logit_view


@logit_view
def handler404(request, *args, **kwargs):
    return render(request, "404.html", {}, status=404)
