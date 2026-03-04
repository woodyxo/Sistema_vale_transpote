from django.contrib import admin
from .models import User, TransportCard, TopUp, Ride, Block


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'cpf', 'status', 'active', 'created_at']
    list_filter = ['status', 'active']
    search_fields = ['name', 'email', 'cpf']
    ordering = ['name']
    readonly_fields = ['id', 'created_at', 'modified_at']


@admin.register(TransportCard)
class TransportCardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'user', 'balance', 'status', 'active', 'created_at']
    list_filter = ['status', 'active']
    search_fields = ['card_number', 'user__name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'modified_at']


@admin.register(TopUp)
class TopUpAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'method', 'date', 'active']
    list_filter = ['method', 'active']
    search_fields = ['user__name']
    ordering = ['-date']
    readonly_fields = ['id', 'created_at', 'modified_at']


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'fare', 'date', 'active']
    list_filter = ['active']
    search_fields = ['user__name', 'card__card_number']
    ordering = ['-date']
    readonly_fields = ['id', 'created_at', 'modified_at']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'active', 'created_at']
    list_filter = ['active']
    search_fields = ['user__name', 'reason']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'modified_at']
