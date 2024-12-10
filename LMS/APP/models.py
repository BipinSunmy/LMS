from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Author(models.Model):
    a_name = models.CharField(max_length=200)
    def __str__(self):
        return self.a_name

class Publication(models.Model):
    publisher = models.CharField(max_length=200)
    def __str__(self):
        return self.publisher

class Category(models.Model):
    category = models.CharField(max_length=200)
    def __str__(self):
        return self.category

class Book(models.Model):
    b_image = models.ImageField()
    title = models.CharField(max_length=200)
    author_id = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=300)
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True)
    dop = models.DateTimeField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
class Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book,on_delete=models.CASCADE)
class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Optional
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user} rented {self.book.title}'

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} purchased {self.book.title}'

class Stock(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    total_quantity = models.PositiveIntegerField(default=0)  # Total books available
    rented_quantity = models.PositiveIntegerField(default=0)  # Books currently rented
    purchased_quantity = models.PositiveIntegerField(default=0)  # Books sold
    
    def available_quantity(self):
        """Calculate available stock for rental or purchase."""
        return self.total_quantity - (self.rented_quantity + self.purchased_quantity)

    def __str__(self):
        return f"Stock for {self.book.title}: {self.available_quantity()} available"
class Payment(models.Model):
    PAYMENT_TYPES = [
        ('subscription', 'Subscription'),
        ('purchase', 'Purchase'),
        ('rental', 'Rental'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='success')  # Simulated

    def __str__(self):
        return f"{self.user.username} - {self.payment_type} - {self.amount} - {self.status}"
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(
        max_length=10, choices=[('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')]
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        """Check if the subscription is still active."""
        return self.end_date > now()  # Correctly using timezone.now()

    def get_subscription_duration(self):
        """Return the duration of the subscription in months."""
        if self.subscription_type == 'silver':
            return 1  # Silver is 1 month
        elif self.subscription_type == 'gold':
            return 3  # Gold is 3 months
        elif self.subscription_type == 'platinum':
            return 12  # Platinum is 12 months
        return 0


    def renewal_price(self):
        """
        Logic for renewal prices:
        - Silver renewal for 3 months will cost more than Gold.
        - The price for Platinum renewal will follow the same logic.
        """
        # Prices for initial subscriptions
        silver_price = 10  # Example: Price for 1 month of Silver
        gold_price = 25    # Example: Price for 3 months of Gold
        platinum_price = 80 # Example: Price for 12 months of Platinum
        
        # Price for renewal logic
        if self.subscription_type == 'silver':
            return gold_price  # Renewing silver for 3 months will cost more than gold
        
        elif self.subscription_type == 'gold':
            return gold_price  # Gold price remains the same for renewals
        
        elif self.subscription_type == 'platinum':
            return platinum_price  # Platinum price remains the same
        
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type} Subscription"
