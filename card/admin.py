from django.contrib import admin
from .models import Card, CardItem
# Register your models here.


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(CardItem)
class CardItemAdmin(admin.ModelAdmin):
    list_display = ['card',  'product', 'amount']
    list_filter = ['product']