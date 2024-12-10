from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms.login import MyLoginForm
from.forms.registration import Registration
from .forms.admin import Addbooks,BookSelectionForm,BookForm,Addauthor,AuthorForm,Adduser,EditUser,SelectUser
from django.contrib.auth import authenticate,login,logout
from .models import Book,Author,Stock,Carts,Payment,Purchase,User,Rental,Subscription
from .forms.user import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import transaction
from .models import Payment
from datetime import datetime, timedelta,timezone
from django.utils.timezone import now

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
    return render(request,"librarian/manageauthor/manageauthor.html")
def manageuser(request):
    return render(request,"librarian/manageuser/manageuser.html")
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

def home(request):
    books = Book.objects.all()
    return render(request,"user/home.html",{"book_list":books})
def book_details(request,id):
    book_detail = get_object_or_404(Book,id= id)
    return render(request,"user/book_details.html",{"book":book_detail})
def select_book(request):
    if request.method == "POST":
        form = BookSelectionForm(request.POST)
        if form.is_valid():
            selected_book = form.cleaned_data['book']
            return redirect('edit_book', book_id=selected_book.id)
    else:
        form = BookSelectionForm()
    return render(request, 'librarian/managebooks/selectbook.html', {'form': form})
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id) 
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)  
        if form.is_valid():
            form.save()  
            return redirect('admin_dashboard')
        form = BookForm(instance=book) 
    return render(request, 'librarian/managebooks/editbooks.html', {'form': form, 'book': book})
def delete_book(request):
    if request.method == "POST":
        # Get the selected book ID from the form
        book_id = request.POST.get("book_id")
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            # Confirmation logic
            confirm = request.POST.get("confirm")
            if confirm == "yes":
                book.delete()
                return redirect("admin_dashboard") 
            else:
                return redirect("delete_book")  
        else:
            return HttpResponse("No book selected.")
    books = Book.objects.all()  
    return render(request, "librarian/managebooks/deletebooks.html", {"books": books})
def addauthor(request):
    if request.method == "POST":
        author = Addauthor(request.POST)
        if author.is_valid():
            author.save()
            return render(request,"librarian/dashboard.html")
    else:
        author = Addauthor()
    return render(request,"librarian/manageauthor/addauthor.html",{"author":author})
from django.shortcuts import render, get_object_or_404, redirect



def editauthor(request):
    authors = Author.objects.all()
    if request.method == "POST":
        author_id = request.POST.get("author_id")
        author_form = AuthorForm(request.POST)
        if author_id:
            author = get_object_or_404(Author,id=author_id)
            if author_form.is_valid():
                author.a_name = author_form.cleaned_data["a_name"]
                author.save()
                return render(request,"librarian/dashboard.html")
    else:
        author_form = AuthorForm()
    return render(request,"librarian/manageauthor/editauthor.html",{"authors":authors,"author_form":author_form})
def adduser(request):
    if request.method == "POST":
        user_form = Adduser(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request,"librarian/dashboard.html")
    else:
        user_form = Adduser()
    return render(request,"librarian/manageuser/adduser.html",{"user_form":user_form})
def edituser(request):
    selected_user = None
    if request.method == "POST":
        # Handle user selection
        if "select_user" in request.POST:
            select_form = SelectUser(request.POST)
            if select_form.is_valid():
                selected_user = select_form.cleaned_data['user']
                edit_form = EditUser(instance=selected_user)
            else:
                edit_form = None
        # Handle user details update
        elif "edit_user" in request.POST:
            user_id = request.POST.get("user_id")
            selected_user = get_object_or_404(User, id=user_id)
            edit_form = EditUser(request.POST, instance=selected_user)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("admin_dashboard")  # Adjust the redirection as needed
    else:
        select_form = SelectUser()
        edit_form = None

    return render(request, "librarian/manageuser/edituser.html", {
        "select_form": select_form,
        "edit_form": edit_form,
        "selected_user": selected_user,
    })
def deleteuser(request):
    selected_user = None

    if request.method == "POST":
        # Handle user selection
        if "select_user" in request.POST:
            select_form = SelectUser(request.POST)
            if select_form.is_valid():
                selected_user = select_form.cleaned_data['user']
        # Handle user deletion
        elif "delete_user" in request.POST:
            user_id = request.POST.get("user_id")
            selected_user = get_object_or_404(User, id=user_id)
            selected_user.delete()
            messages.success(request, f"User '{selected_user.username}' has been deleted.")
            return redirect("admin_dashboard") 
    else:
        select_form = SelectUser()

    return render(request, "librarian/manageuser/deleteuser.html", {
        "select_form": select_form,
        "selected_user": selected_user,
    })
def user_profile(request):
    # Example: fetching a user object or data related to the user
    user = request.user  # Assuming you're using Django's built-in user model
    return render(request, 'user/user_profile.html', {'user': user})
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
def cart(request):
    # Retrieve the cart items for the logged-in user
    cart_items = Carts.objects.filter(user=request.user)
    
    # Check stock availability for each item
    for cart_item in cart_items:
        book_stock = get_object_or_404(Stock, book=cart_item.book)
        cart_item.available_stock = book_stock.available_quantity()  # Add available stock to cart item

    # Calculate the total price for the cart, considering the quantity
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    
    # Render the cart page with the cart items and total price
    return render(request, 'user/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Check if the book is already in the user's cart
    cart_item, created = Carts.objects.get_or_create(user=request.user, book=book)
    if not created:
        # If already in cart, increase quantity by 1
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Carts, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Carts, id=cart_item_id, user=request.user)
    
    # Check the action (increase or decrease)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1  # Prevent going below 1
    
    cart_item.save()

    return redirect('cart')  
def purchase_book(request, book_id):
    # Get the book and its stock details
    book = get_object_or_404(Book, id=book_id)
    stock = get_object_or_404(Stock, book=book)

    if request.method == "POST":
        try:
            # Get the requested quantity from the form
            requested_quantity = int(request.POST.get("quantity", 1))

            # Check if enough stock is available
            if stock.available_quantity() >= requested_quantity:
                total_amount = book.price * requested_quantity

                with transaction.atomic():
                    # Update stock quantities
                    stock.purchased_quantity += requested_quantity
                    stock.save()

                    # Create a record in the Purchase table
                    Purchase.objects.create(
                        user=request.user,
                        book=book,
                        purchased_at=now(),
                    )

                    # Simulate payment success
                    messages.success(request, f"Purchase successful! You bought {requested_quantity} copies of '{book.title}' for {total_amount}.")

                    return redirect("home")
            else:
                messages.error(request, f"Not enough stock available. Only {stock.available_quantity()} left.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("purchase_book", book_id=book_id)

    return render(request, "user/purchase_book.html", {"book": book, "stock": stock, "available_stock": stock.available_quantity()})
def make_payment(request):
    # Get cart items
    cart_items = Carts.objects.filter(user=request.user)
    
    # Initialize total amount for cart or individual book
    total_amount = 0
    payment_type = request.GET.get("payment_type", "purchase")
    book = None
    requested_quantity = 0

    # Check if cart is not empty
    if cart_items.exists():
        # If there are items in the cart, calculate total amount
        for cart_item in cart_items:
            book = cart_item.book
            stock = get_object_or_404(Stock, book=book)
            if payment_type == "purchase":
                total_amount += book.price * cart_item.quantity
            elif payment_type == "rent":
                total_amount += book.rental_price * cart_item.quantity
    else:
        # If cart is empty, handle a single book payment
        book_id = request.GET.get("book_id")
        if not book_id:
            messages.error(request, "Invalid book.")
            return redirect("home")
        
        book = get_object_or_404(Book, id=book_id)
        stock = get_object_or_404(Stock, book=book)
        requested_quantity = int(request.GET.get("quantity", 1))
        
        if payment_type == "purchase":
            total_amount = book.price * requested_quantity
        elif payment_type == "rent":
            total_amount = (book.price//10) * requested_quantity

    if request.method == "POST":
        # Extract card details
        card_number = request.POST.get("card_number")
        card_expiry = request.POST.get("card_expiry")
        card_cvv = request.POST.get("card_cvv")

        # Validate card details
        if not (card_number and card_expiry and card_cvv):
            messages.error(request, "Please provide all payment details.")
            return redirect("make_payment")

        # Validate stock availability (cart or single book)
        if cart_items.exists():
            for cart_item in cart_items:
                stock = get_object_or_404(Stock, book=cart_item.book)
                if stock.available_quantity() < cart_item.quantity:
                    messages.error(request, f"Not enough stock for {cart_item.book.title}. Only {stock.available_quantity()} left.")
                    return redirect("cart")
        else:
            if stock.available_quantity() < requested_quantity:
                messages.error(request, f"Not enough stock for {book.title}. Only {stock.available_quantity()} left.")
                return redirect("home")

        # Proceed with payment processing
        if len(card_number) == 16 and len(card_cvv) == 3:
            try:
                with transaction.atomic():  # Start the transaction block
                    # Record the payment
                    payment = Payment.objects.create(
                        user=request.user,
                        payment_type=payment_type,
                        amount=total_amount,
                        status="success",  # Initially assuming success
                    )

                    # Process cart payment
                    if cart_items.exists():
                        for cart_item in cart_items:
                            stock = get_object_or_404(Stock, book=cart_item.book)
                            if payment_type == "purchase":
                                stock.purchased_quantity += cart_item.quantity
                                Purchase.objects.create(
                                    user=request.user,
                                    book=cart_item.book,
                                    purchased_at=datetime.now(),
                                )
                            elif payment_type == "rent":
                                stock.rented_quantity += cart_item.quantity
                                Rental.objects.create(
                                    user=request.user,
                                    book=cart_item.book,
                                    rented_at=datetime.now(),
                                    due_date=datetime.now() + timedelta(days=14)
                                )
                            stock.save()  # Update stock after purchase or rent
                        Carts.objects.filter(user=request.user).delete()  # Clear the cart after purchase/rent
                        messages.success(request, "Cart payment successful!")
                    
                    # Process individual book payment
                    else:
                        if payment_type == "purchase":
                            stock.purchased_quantity += requested_quantity
                            Purchase.objects.create(
                                user=request.user,
                                book=book,
                                purchased_at=datetime.now(),
                            )
                        elif payment_type == "rent":
                            stock.rented_quantity += requested_quantity
                            Rental.objects.create(
                                user=request.user,
                                book=book,
                                rented_at=datetime.now(),
                                due_date=datetime.now() + timedelta(days=14)
                            )
                        stock.save()  # Update stock after purchase or rent
                        messages.success(request, f"Payment for {book.title} successful!")

                    return redirect("home")

            except Exception as e:
                # If anything fails in the transaction, rollback everything
                messages.error(request, f"An error occurred during the payment process: {str(e)}")
                return redirect("make_payment")

        else:
            # Handle invalid card details
            Payment.objects.create(
                user=request.user,
                payment_type=payment_type,
                amount=total_amount,
                status="failed",
            )
            messages.error(request, "Payment failed. Please check your card details.")
            return redirect("make_payment")

    # Render the payment page with either cart items or a single book
    return render(request, "payment/make_payment.html", {
        "payment_type": payment_type,
        "total_amount": total_amount,
        "cart_items": cart_items,
        "book": book if not cart_items.exists() else None,
    })

def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    stock = get_object_or_404(Stock, book=book)

    if request.method == "POST":
        requested_quantity = int(request.POST.get("quantity", 1))

        if stock.available_stock >= requested_quantity:
            try:
                with transaction.atomic():
                    # Update stock
                    stock.rented_quantity += requested_quantity
                    stock.total_quantity -= requested_quantity
                    stock.save()

                    # Record rent in payment history
                    Payment.objects.create(
                        user=request.user,
                        payment_type="rent",
                        amount=book.rental_price * requested_quantity,
                        status="success"
                    )

                    messages.success(request, f"You successfully rented {requested_quantity} copies of '{book.title}'!")
            except Exception as e:
                messages.error(request, f"An error occurred during the rental: {e}")
        else:
            messages.error(request, f"Not enough stock available to rent. Only {stock.available_stock} left.")

        return redirect("home")

    return render(request, "user/rent_book.html", {"book": book, "stock": stock})
from django.db import transaction

def subscribe_view(request):
    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type')
        cost = 0

        # Determine subscription duration and cost
        if subscription_type == 'silver':
            duration = timedelta(days=30)  # 1 month
            cost = 29
        elif subscription_type == 'gold':
            duration = timedelta(days=90)  # 3 months
            cost = 80
        elif subscription_type == 'platinum':
            duration = timedelta(days=365)  # 1 year
            cost = 300
        else:
            messages.error(request, "Invalid subscription type selected.")
            return redirect('subscribe')  # Redirect back to subscription page

        # Calculate end date
        end_date = now() + duration
    return render(request, "user/subscribe.html")
def sub_payment(request):
    # Retrieve query parameters
    amount = request.GET.get('amount')
    payment_type = request.GET.get('payment_type')
    if payment_type == 'silver':
        duration = timedelta(days=30)  # 1 month
        cost = 29
    elif payment_type == 'gold':
        duration = timedelta(days=90)  # 3 months
        cost = 80
    elif payment_type == 'platinum':
        duration = timedelta(days=365)  # 1 year
        cost = 300
    end_date = now() + duration
    if not amount or not payment_type:
        messages.error(request, "Invalid payment details.")
        return redirect('home')

    if request.method == 'POST':
        # Simulate payment process
        # Payment functionality
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvv = request.POST.get('card_cvv')
        if not (card_number and card_expiry and card_cvv):
            messages.error(request, "Please provide valid payment details.")
            return redirect('subscribe')
        # Simulate card validation
        if len(card_number) == 16 and len(card_cvv) == 3:
            # Create a payment entry
            Payment.objects.create(
                user=request.user,
                payment_type="subscription",
                amount=amount,
                status="success"
            )
            # Create or update subscription
            subscription, created = Subscription.objects.get_or_create(
                    user=request.user,
                    defaults={'subscription_type': payment_type, 'end_date': end_date}
                )

            if created:
                # If a new subscription was created
                messages.success(request, f"Welcome! You've successfully subscribed to the {payment_type.capitalize()} plan.")
            else:
                # If updating an existing subscription
                subscription.subscription_type = payment_type
                subscription.end_date = end_date
                subscription.save()
                messages.success(request, f"Subscription updated to the {payment_type.capitalize()} plan.")

            messages.success(request, f"Subscription to {payment_type} plan successful!")
            return redirect('home')
        else:
            messages.error(request, "Payment failed. Invalid card details.")
            return redirect('subscribe')
    return render(request, "payment/make_payment.html", {
        "amount": amount,
        "payment_type": payment_type,
    })
