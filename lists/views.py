from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.
def home_page(request):
    """主页视图"""
    return render(request,'lists/home.html')

def view_list(request):
    """待办事项视图"""
    items=Item.objects.all()
    return render(request,'lists/list.html',{'items':items})

def new_list(request):
    list_=List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
