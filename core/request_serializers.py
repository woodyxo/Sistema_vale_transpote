from rest_framework import serializers
from core.models import User, TransportCard, Ride, TopUp, Block
import random
import string


# ─── User ─────────────────────────────────────────────────────────────────────

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar/atualizar Usuários (POST / PATCH).
    Inclui o campo password (write_only) e valida CPF único.
    """
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'cpf', 'status', 'active']
        read_only_fields = ['id']

    def validate_cpf(self, value):
        # Remove caracteres não numéricos para validação de tamanho
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor não pode ser zero ou negativo.")
        return value


# ─── TransportCard ────────────────────────────────────────────────────────────

class TransportCardCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar/atualizar Cartões (POST / PATCH).
    Gera o número do cartão automaticamente se não fornecido.
    """

    class Meta:
        model = TransportCard
        fields = ['id', 'user', 'card_number', 'balance', 'status', 'active']
        read_only_fields = ['id']
        extra_kwargs = {
            'card_number': {'required': False},
        }

    def validate(self, attrs):
        # Garante que cada usuário só tem um cartão
        user = attrs.get('user')
        if user and not self.instance:
            if TransportCard.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    {"user": "Este usuário já possui um cartão de transporte."}
                )
        return attrs

    def create(self, validated_data):
        # Gera número único do cartão se não foi fornecido
        if not validated_data.get('card_number'):
            validated_data['card_number'] = self._generate_card_number()
        return super().create(validated_data)

    def _generate_card_number(self):
        """Gera um número de cartão único no formato XXXX-XXXX-XXXX"""
        while True:
            number = '-'.join(
                ''.join(random.choices(string.digits, k=4)) for _ in range(3)
            )
            if not TransportCard.objects.filter(card_number=number).exists():
                return number


# ─── Ride ─────────────────────────────────────────────────────────────────────

class RideCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para registrar uma Viagem (POST).

    Regras de negócio verificadas aqui:
    1. O cartão deve estar ativo (status = 'active').
    2. Não pode existir bloqueio ativo para o usuário.
    3. Deve haver saldo suficiente para pagar a passagem.
    4. Ao criar, desconta o valor do saldo automaticamente.
    """

    class Meta:
        model = Ride
        fields = ['id', 'user', 'card', 'fare', 'latitude', 'longitude']
        read_only_fields = ['id']

    def validate(self, attrs):
        card = attrs.get('card')
        user = attrs.get('user')
        fare = attrs.get('fare')

        # Regra 1: cartão deve estar ativo
        if card.status != 'active':
            raise serializers.ValidationError(
                {"card": "O cartão está bloqueado e não pode ser usado para viagens."}
            )

        # Regra 2: usuário não pode ter bloqueio ativo
        if Block.objects.filter(user=user, active=True).exists():
            raise serializers.ValidationError(
                {"user": "Este usuário está bloqueado e não pode registrar viagens."}
            )

        # Regra 3: saldo suficiente
        if card.balance < fare:
            raise serializers.ValidationError(
                {"fare": f"Saldo insuficiente. Saldo atual: R${card.balance}. Passagem: R${fare}."}
            )

        return attrs

    def create(self, validated_data):
        card = validated_data['card']
        fare = validated_data['fare']

        # Regra 4: desconta o saldo ao registrar a viagem
        card.balance -= fare
        card.save()

        return super().create(validated_data)


# ─── TopUp ────────────────────────────────────────────────────────────────────

class TopUpCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar uma Recarga (POST).

    Regras de negócio:
    - O valor não pode ser negativo ou zero.
    - Ao criar, aumenta o saldo do cartão automaticamente.
    """

    class Meta:
        model = TopUp
        fields = ['id', 'user', 'amount', 'method']
        read_only_fields = ['id']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor da recarga deve ser positivo.")
        return value

    def create(self, validated_data):
        user = validated_data['user']
        amount = validated_data['amount']

        # Aumenta o saldo do cartão automaticamente
        try:
            card = user.card  # OneToOne
            card.balance += amount
            card.save()
        except TransportCard.DoesNotExist:
            raise serializers.ValidationError(
                {"user": "Este usuário não possui cartão de transporte cadastrado."}
            )

        return super().create(validated_data)


# ─── Block ────────────────────────────────────────────────────────────────────

class BlockCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar/atualizar um Bloqueio (POST / PATCH).
    Ao criar um bloqueio, atualiza o status do cartão para 'blocked'.
    Ao desativar (PATCH active=False), reativa o cartão.
    """

    class Meta:
        model = Block
        fields = ['id', 'user', 'reason', 'active']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = validated_data['user']
        block = super().create(validated_data)

        # Bloqueia o cartão ao criar bloqueio ativo
        if block.active:
            try:
                card = user.card
                card.status = 'blocked'
                card.save()
            except TransportCard.DoesNotExist:
                pass

        return block

    def update(self, instance, validated_data):
        block = super().update(instance, validated_data)

        # Se o bloqueio foi desativado, reativa o cartão
        if not block.active:
            try:
                card = block.user.card
                # Só reativa se não houver outros bloqueios ativos
                outros_bloqueios = Block.objects.filter(
                    user=block.user, active=True
                ).exclude(pk=block.pk).exists()

                if not outros_bloqueios:
                    card.status = 'active'
                    card.save()
            except TransportCard.DoesNotExist:
                pass

        return block
