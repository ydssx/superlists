from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def home_page(request):
    """主页视图"""
    return HttpResponse('<html><title>To-Do lists</title></html>')