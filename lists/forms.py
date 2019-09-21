from django.forms import ModelForm
from django import forms
from lists.models import Item

class ItemForm(ModelForm):
    
    class Meta:
        model=Item
        fields=('text',)
        widgets={
            'text':forms.fields.TextInput(attrs={'placeholder':'Enter a to-do item','class':'form-control input-lg'})}
        error_messages={'text':{'required':"表单提交不能为空！"}}