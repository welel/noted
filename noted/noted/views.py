from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'privacy_policy.html', {})


def handler404(request, *args, **kwargs):
    return render(request, '404.html', {}, status=404)
