from django import forms
from ..models import Book
class Addbooks(forms.ModelForm):
    dop = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    class Meta:
        model = Book
        fields = ('b_image','title','description','price','author_id','category','publication')