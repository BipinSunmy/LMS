from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms.login import MyLoginForm
from.forms.registration import Registration
from .forms.admin import Addbooks
from django.contrib.auth import authenticate,login,logout
from .models import Book
from .models import Subscription
from .models import Cart
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.contrib import messages

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


@login_required
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
    return render(request, 'user/user_profile.html', {'user': user})

from .forms.user import EditProfileForm  # Import the profile edit form

@login_required
def edit_profile(request):
    user = request.user  # Get the currently logged-in user
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user data
            return redirect('user_profile')  # Redirect to the user's profile page
    else:
        form = EditProfileForm(instance=user)  # Pre-populate the form with the user's data
    
    return render(request, 'user/edit_profile.html', {'form': form})

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('user_profile')  # Redirect to user profile page after successful change
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user/change_password.html', {'form': form})


def wishlist(request):
    # Your view logic here
    return render(request, 'user/wishlist.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def cart(request):
    # Retrieve the cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate the total price for the cart, considering the quantity
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    
    # Render the cart page with the cart items and total price
    return render(request, 'user/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if the book is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        # If already in cart, increase quantity by 1
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')  # Redirect to the cart page

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    # Check the action (increase or decrease)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1  # Prevent going below 1
    
    cart_item.save()

    return redirect('cart')  # Redirect to the cart page@login_required

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

@login_required
def make_payment(request):
    # Automatically populate payment_type and amount
    payment_type = request.GET.get("payment_type", "purchase")  # Default to "purchase"
    amount = request.GET.get("amount", 0)  # Default to 0 if not provided
    
    if request.method == "POST":
        # Extract card details from form
        card_number = request.POST.get("card_number")
        card_expiry = request.POST.get("card_expiry")
        card_cvv = request.POST.get("card_cvv")

        # Validate card details
        if not (card_number and card_expiry and card_cvv):
            messages.error(request, "Please provide all payment details.")
            return redirect("make_payment")

        if len(card_number) == 16 and len(card_cvv) == 3:
            # Payment successful, record it
            Payment.objects.create(
                user=request.user,
                payment_type=payment_type,
                amount=float(amount),
                status="success"
            )
            
            # If this is a cart payment, clear the cart
            if payment_type == "purchase":
                Cart.objects.filter(user=request.user).delete()

            messages.success(request, "Payment successful!")
            return redirect("home")
        else:
            # Payment failed, record it
            Payment.objects.create(
                user=request.user,
                payment_type=payment_type,
                amount=float(amount),
                status="failed"
            )
            messages.error(request, "Payment failed. Please check your card details.")
            return redirect("make_payment")

    # Render payment form with populated data
    return render(request, "payment/make_payment.html", {
        "payment_type": payment_type,
        "amount": amount,
    })




