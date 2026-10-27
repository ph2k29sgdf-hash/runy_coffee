from django.contrib import admin
from .models import Product, Location, Operator, Order, SupportMessage, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_new', 'image')
    list_filter = ('category', 'is_seasonal', 'is_new')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_new')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'working_hours')

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'location')
    list_filter = ('location',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'items_summary', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'phone')

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'created_at')
    list_filter = ('rating', 'location')
    search_fields = ('name', 'text')
