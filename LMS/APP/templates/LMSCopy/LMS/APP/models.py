from django.db import models
from django.contrib.auth.models import User

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
    author_id = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    description = models.CharField(max_length=300)
    publication = models.ForeignKey(Publication,on_delete=models.SET_NULL,null=True)
    dop = models.DateTimeField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True  )
    def __str__(self):
        return self.title
class Whislist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book,on_delete=models.CASCADE)
class Cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book,on_delete=models.CASCADE)
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