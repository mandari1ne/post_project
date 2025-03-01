from django.shortcuts import render

# Create your views here.

def users_index(request):
    return render(request, 'users_index.html')
