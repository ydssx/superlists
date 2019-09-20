from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Item, List

# Create your views here.
def home_page(request):
    """主页视图"""
    return render(request,'lists/home.html')

def view_list(request,list_id):
    """待办事项视图"""
    list_=List.objects.get(id=list_id)
    error=None

    if request.method=='POST':
        try:
            item=Item.objects.create(text=request.POST['item_text'],list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error="表单提交不能为空！"
    return render(request,'lists/list.html',{'list':list_, 'error':error})

def new_list(request):
    list_=List.objects.create()
    item=Item.objects.create(text=request.POST['item_text'],list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error="表单提交不能为空！"
        return render(request,'lists/home.html',{'error':error})
    return redirect(list_)
