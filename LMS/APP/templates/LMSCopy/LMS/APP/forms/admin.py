from django import forms
from ..models import Book
class Addbooks(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('b_image','title','description','dop','price','author_id','category','publication')