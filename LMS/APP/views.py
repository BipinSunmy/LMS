from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms.login import MyLoginForm
from django.contrib.auth import authenticate,login
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
                login(request,auth_user)
                # group = auth_user.groups.first()
                # group_name = group.name if group else "No Group"
                # request.session['group_name'] = group_name
                return redirect("home")
            else:
                return HttpResponse("Not Authenticated")
    else:
        login_form = MyLoginForm()
    return render(request,"useraccount/login.html",{"login_form":login_form})