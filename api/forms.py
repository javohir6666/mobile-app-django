from django import forms
from .models import Todo
class TodoForm(forms.ModelForm):
    title=forms.CharField(
        label='Title',
        widget=(forms.TextInput(attrs={
            'class':'form-control',
            'rows': '3',
            'placeholder':'Type here...'
        }))
    )
    desc = forms.CharField(
        label= 'Description',
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'rows':'3',
            'placeholder':"Say Something..."
        })
        
    )
    class Meta:
        model = Todo
        fields = ['title','desc']
        