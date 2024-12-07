from django.contrib import admin
from .models import Author,Category,Book,Publication

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Publication)