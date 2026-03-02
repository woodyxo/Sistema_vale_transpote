from django.contrib import admin
from core.models import User, TransportCard, Ride, TopUp, Block


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'cpf', 'status', 'active', 'created_at']
    list_filter = ['status', 'active']
    search_fields = ['name', 'email', 'cpf']


@admin.register(TransportCard)
class TransportCardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'user', 'balance', 'status', 'active']
    list_filter = ['status', 'active']
    search_fields = ['card_number', 'user__name']


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'fare', 'date', 'latitude', 'longitude']
    list_filter = ['date']
    search_fields = ['user__name', 'card__card_number']


@admin.register(TopUp)
class TopUpAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'method', 'date']
    list_filter = ['method', 'date']
    search_fields = ['user__name']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'active', 'created_at']
    list_filter = ['active']
    search_fields = ['user__name', 'reason']
