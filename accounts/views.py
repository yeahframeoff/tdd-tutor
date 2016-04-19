from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


# Create your views here.
def persona_login(request):
    user = authenticate(assertion=request.POST['assertion'])
    if user:
        login(request, user)
        return HttpResponse('OK')
    return HttpResponse()
