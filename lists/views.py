from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    """主页视图"""
    return render(request,'lists/home.html',{'form':ItemForm()})

def view_list(request,list_id):
    """待办事项视图"""
    list_=List.objects.get(id=list_id)
    form=ItemForm()
    if request.method=='POST':
        form=ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request,'lists/list.html',{'list':list_,"form":form})

def new_list(request):
    form=ItemForm(data=request.POST)
    if form.is_valid():
        list_=List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request,'lists/home.html',{"form":form})
    
