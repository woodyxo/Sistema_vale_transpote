from rest_framework import serializers
from core.models import User, TransportCard, Ride, TopUp, Block


# ─── User ─────────────────────────────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    """Serializer padrão para leitura de Usuários (GET)"""

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'cpf', 'status',
            'active', 'created_at', 'modified_at'
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']
        # password NÃO é exposto nas respostas


# ─── TransportCard ────────────────────────────────────────────────────────────

class TransportCardSerializer(serializers.ModelSerializer):
    """Serializer padrão para leitura de Cartões (GET)"""
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = TransportCard
        fields = [
            'id', 'user', 'user_name', 'card_number',
            'balance', 'status', 'active', 'created_at', 'modified_at'
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


# ─── Ride ─────────────────────────────────────────────────────────────────────

class RideSerializer(serializers.ModelSerializer):
    """Serializer padrão para leitura de Viagens (GET)"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    card_number = serializers.CharField(source='card.card_number', read_only=True)

    class Meta:
        model = Ride
        fields = [
            'id', 'user', 'user_name', 'card', 'card_number',
            'fare', 'date', 'latitude', 'longitude',
            'active', 'created_at', 'modified_at'
        ]
        read_only_fields = ['id', 'date', 'created_at', 'modified_at']


# ─── TopUp ────────────────────────────────────────────────────────────────────

class TopUpSerializer(serializers.ModelSerializer):
    """Serializer padrão para leitura de Recargas (GET)"""
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = TopUp
        fields = [
            'id', 'user', 'user_name', 'amount',
            'method', 'date', 'active', 'created_at', 'modified_at'
        ]
        read_only_fields = ['id', 'date', 'created_at', 'modified_at']


# ─── Block ────────────────────────────────────────────────────────────────────

class BlockSerializer(serializers.ModelSerializer):
    """Serializer padrão para leitura de Bloqueios (GET)"""
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Block
        fields = [
            'id', 'user', 'user_name', 'reason',
            'active', 'created_at', 'modified_at'
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']
