from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms.login import MyLoginForm
from.forms.registration import Registration
from .forms.admin import Addbooks
from django.contrib.auth import authenticate,login,logout
from .models import Book

# Create your views here.

def Display(request):
    return HttpResponse("Hello")

def user_login(request):
    if request.method == "POST":
        login_form = MyLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            auth_user = authenticate(request,username=cleaned_data["username"],password = cleaned_data["password"])
            if auth_user is not None:
                if auth_user.is_staff == 1:
                    login(request,auth_user)
                    # group = auth_user.groups.first()
                    # group_name = group.name if group else "No Group"
                    # request.session['group_name'] = group_name
                    return redirect("admin_dashboard")
                else:
                    return redirect("home")
            else:
                return HttpResponse("Not Authenticated")
    else:
        login_form = MyLoginForm()
    return render(request,"useraccount/login.html",{"login_form":login_form})
def user_logout(request):
    logout(request)
    return redirect("home")
def admin_dashboard(request):
    return render(request,"librarian/dashboard.html")
def registration_view(request):
    if request.method == "POST":
        regis_form = Registration(request.POST)
        if regis_form.is_valid():
            new_user = regis_form.save(commit=False)
            new_user.set_password(regis_form.cleaned_data["password"])
            new_user.save()
            return render(request,"useraccount/register_done.html")
    else:
        regis_form = Registration()
    return render(request,"useraccount/registration.html",{"regis_form":regis_form})
def managebooks_view(request):
    return render(request,"librarian/managebooks/managebooks.html")
def manageauthor_view(request):
    return render(request,"librarian/manageauthor.html")
def manageuser(request):
    return render(request,"librarian/manageuser.html")
def addbook(request):
    book_d = Addbooks()
    return render(request,"librarian/managebooks/addbooks.html",{"book_form":book_d})
def home(request):
    books = Book.objects.all()
    return render(request,"user/home.html",{"book_list":books})
def book_details(request,id):
    book_detail = get_object_or_404(Book,id= id)
    return render(request,"user/book_details.html",{"book":book_detail})