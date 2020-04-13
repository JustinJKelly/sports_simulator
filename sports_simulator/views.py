from django.shortcuts import redirect, render

def home(request):
    #populate()
    return render(request, 'base.html')