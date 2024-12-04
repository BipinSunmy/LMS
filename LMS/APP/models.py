from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    a_name = models.CharField(max_length=200)
class Publication(models.Model):
    publisher = models.CharField(max_length=200)
class Category(models.Model):
    category = models.CharField(max_length=200)
class Book(models.Model):
    b_image = models.ImageField()
    title = models.CharField(max_length=200)
    author_id = models.ForeignKey(Author,on_delete=models.SET_NULL)
    description = models.CharField(max_length=300)
    publication = models.ForeignKey(Publication,on_delete=models.SET_NULL)
    dop = models.DateTimeField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL)
class Whislist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book,on_delete=models.CASCADE)
class Cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book,on_delete=models.CASCADE)



