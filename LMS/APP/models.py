from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book, on_delete=models.CASCADE)

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book, on_delete=models.CASCADE)

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

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(
        max_length=10, choices=[('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')]
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        """Check if the subscription is still active."""
        return self.end_date > timezone.now()  # Correctly using timezone.now()

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
