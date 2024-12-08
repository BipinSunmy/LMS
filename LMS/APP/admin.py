from django.contrib import admin
from .models import Author,Category,Book,Publication,Stock

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Publication)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('book', 'total_quantity', 'rented_quantity', 'purchased_quantity', 'available_quantity')
    readonly_fields = ('available_quantity',)
    search_fields = ('book__title',)  # Allows searching by book title
    list_filter = ('book',)  # Filter by book
