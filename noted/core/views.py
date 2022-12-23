from django.shortcuts import render


def handler404(request, *args, **kwargs):
    return render(request, "404.html", {}, status=404)
