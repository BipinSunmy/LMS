from django import forms
from ..models import Book,Author,User
class Addbooks(forms.ModelForm):
    dop = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    class Meta:
        model = Book
        fields = ('b_image','title','description','dop','price','author_id','category','publication')
        widgets = {'dop': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),}
class BookSelectionForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select a Book to Edit"
    )
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('b_image', 'title', 'description', 'price', 'author_id', 'category', 'publication', 'dop')
        widgets = {
            'dop': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
class Addauthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('a_name',)

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('a_name',)
class Adduser(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm_password",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password doesnt match')
        return cd['password2']
class SelectUser(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select User"
    )
class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
