import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email as _validate_email
from django.http import JsonResponse

from account.models import User
from account.auth import send_signup_link


def send_singup_email(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == "POST" and is_ajax:
        email = json.load(request).get('email', None)
        try:
            _validate_email(email)
        except ValidationError as e:
            return JsonResponse({'msg': 'invalid'}, status=200)
        else:
            success = send_signup_link(email)
            if success:
                return JsonResponse({'msg': 'sent'}, status=200)
    return JsonResponse({'msg': 'error'}, status=200)


def validate_email(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == "GET" and is_ajax:
        email = request.GET.get('email', None)
        response = {'is_taken': User.objects.filter(email=email).exists()}
        return JsonResponse(response, status=200)
    return JsonResponse({'is_taken': 'error'}, status=200)


def signup(request):
    return JsonResponse({'SIGNUP': 'OK'}, status=200)
