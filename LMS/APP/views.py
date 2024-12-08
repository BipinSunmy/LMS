from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms.login import MyLoginForm
from.forms.registration import Registration
from .forms.admin import Addbooks
from django.contrib.auth import authenticate,login,logout
from .models import Book
from .models import Subscription
from django.contrib.auth.decorators import login_required

# Create your views here.

def Display(request):
    return HttpResponse("Hello")

def user_login(request):
    if request.method == "POST":
        login_form = MyLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            auth_user = authenticate(request, username=cleaned_data["username"], password=cleaned_data["password"])
            if auth_user is not None:
                login(request, auth_user)
                # Redirect user to the homepage or any page based on subscription status
                if auth_user.is_staff:
                    return redirect("admin_dashboard")

                else:
                    return redirect("home")
            else:
                return HttpResponse("Invalid Credentials")
    else:
        login_form = MyLoginForm()
    return render(request, "useraccount/login.html", {"login_form": login_form})


def user_logout(request):
    logout(request)
    return redirect("home")  # Redirect to the homepage after logout

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
    if request.method == "POST":
        book_d = Addbooks(request.POST,request.FILES)
        if book_d.is_valid():
            book_isn = book_d.save(commit=False)
            book_isn.dop = book_d.cleaned_data["dop"]
            book_isn.save()
            return render(request,"librarian/managebooks/addbooks.html")
    else:
        book_d = Addbooks()
    return render(request,"librarian/managebooks/addbooks.html",{"book_form":book_d})

@login_required
def home(request):
    subscription = None
    books = Book.objects.all()  # Fetch all books, both for subscribers and non-subscribers

    try:
        # Attempt to fetch the user's subscription
        subscription = Subscription.objects.get(user=request.user)
        if not subscription.is_active:
            # If the subscription is inactive, the user will still see the books but with limited functionality
            pass
    except Subscription.DoesNotExist:
        # If no subscription exists, the user will still see the books but with limited functionality
        pass

    return render(request, "user/home.html", {"book_list": books, "subscription": subscription})




def book_details(request,id):
    book_detail = get_object_or_404(Book,id= id)
    return render(request,"user/book_details.html",{"book":book_detail})

from datetime import timedelta
from django.utils import timezone

def subscribe_user(request):
    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type')
        if subscription_type == 'silver':
            duration = timedelta(days=30)  # 1 month
        elif subscription_type == 'gold':
            duration = timedelta(days=90)  # 3 months
        else:
            duration = timedelta(days=365)  # 1 year
        
        # Calculate end date
        end_date = timezone.now() + duration

        # Create a subscription entry
        Subscription.objects.create(user=request.user, subscription_type=subscription_type, end_date=end_date)
        
        # Redirect user or show success message
        return redirect('home')
    
from django.shortcuts import render

# Define your view for the user profile
def user_profile(request):
    # Example: fetching a user object or data related to the user
    user = request.user  # Assuming you're using Django's built-in user model
    return render(request, 'user_profile.html', {'user': user})

def wishlist(request):
    # Your view logic here
    return render(request, 'user/wishlist.html')

def cart(request):
    # Your cart logic here
    return render(request, 'user/cart.html')  # Update template name if necessary

from django.shortcuts import render

@login_required
def subscribe_view(request):
    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type')
        if subscription_type == 'silver':
            duration = timedelta(days=30)  # 1 month
        elif subscription_type == 'gold':
            duration = timedelta(days=90)  # 3 months
        else:
            duration = timedelta(days=365)  # 1 year
        
        # Calculate end date
        end_date = timezone.now() + duration

        # Create a subscription entry
        Subscription.objects.create(user=request.user, subscription_type=subscription_type, end_date=end_date)
        
        # Redirect user or show success message
        return redirect('home')

    return render(request, "user/subscribe.html")





