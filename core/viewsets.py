from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count

from core.models import User, TransportCard, Ride, TopUp, Block
from core.serializers import (
    UserSerializer, TransportCardSerializer,
    RideSerializer, TopUpSerializer, BlockSerializer
)
from core.request_serializers import (
    UserCreateSerializer, TransportCardCreateSerializer,
    RideCreateSerializer, TopUpCreateSerializer, BlockCreateSerializer
)
from core.filters import (
    UserFilter, TransportCardFilter,
    RideFilter, TopUpFilter, BlockFilter
)


# ─── User ViewSet ─────────────────────────────────────────────────────────────

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Usuários.

    GET    /api/users/       → lista todos
    POST   /api/users/       → cria novo usuário
    GET    /api/users/{id}/  → detalha um usuário
    PATCH  /api/users/{id}/  → atualiza parcialmente
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['name', 'email', 'cpf']
    ordering_fields = ['name', 'created_at', 'status']
    ordering = ['name']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return UserCreateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        """Exclusão lógica: marca como inativo em vez de apagar."""
        instance.active = False
        instance.save()


# ─── TransportCard ViewSet ────────────────────────────────────────────────────

class TransportCardViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Cartões de Transporte.

    GET    /api/cards/       → lista todos
    POST   /api/cards/       → cria novo cartão
    GET    /api/cards/{id}/  → detalha um cartão
    PATCH  /api/cards/{id}/  → atualiza parcialmente
    """
    queryset = TransportCard.objects.select_related('user').all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TransportCardFilter
    search_fields = ['card_number', 'user__name']
    ordering_fields = ['balance', 'created_at', 'status']
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TransportCardCreateSerializer
        return TransportCardSerializer

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


# ─── Ride ViewSet ─────────────────────────────────────────────────────────────

class RideViewSet(viewsets.ModelViewSet):
    """
    ViewSet para registrar e consultar Viagens.

    GET  /api/rides/          → lista todas as viagens
    POST /api/rides/          → registra nova viagem (aplica regras de negócio)
    GET  /api/rides/{id}/     → detalha uma viagem

    Ação extra:
    GET  /api/rides/report/   → relatório: total gasto, viagens por usuário
    """
    queryset = Ride.objects.select_related('user', 'card').all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RideFilter
    search_fields = ['user__name', 'card__card_number']
    ordering_fields = ['date', 'fare']
    ordering = ['-date']
    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return RideCreateSerializer
        return RideSerializer

    @action(detail=False, methods=['get'])
    def report(self, request):
        """
        GET /api/rides/report/
        Retorna relatório de uso: total gasto, usuários que mais viajam.
        """
        total_fare = Ride.objects.aggregate(total=Sum('fare'))['total'] or 0

        top_users = (
            Ride.objects
            .values('user__id', 'user__name')
            .annotate(total_rides=Count('id'), total_spent=Sum('fare'))
            .order_by('-total_rides')[:10]
        )

        return Response({
            'total_fare_all_rides': total_fare,
            'top_users': list(top_users),
        })


# ─── TopUp ViewSet ────────────────────────────────────────────────────────────

class TopUpViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Recargas.

    GET  /api/topups/   → lista todas as recargas
    POST /api/topups/   → cria recarga e aumenta saldo automaticamente
    """
    queryset = TopUp.objects.select_related('user').all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TopUpFilter
    search_fields = ['user__name']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']
    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return TopUpCreateSerializer
        return TopUpSerializer


# ─── Block ViewSet ────────────────────────────────────────────────────────────

class BlockViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Bloqueios de cartão.

    GET    /api/blocks/       → lista todos os bloqueios
    POST   /api/blocks/       → cria bloqueio (bloqueia cartão automaticamente)
    GET    /api/blocks/{id}/  → detalha um bloqueio
    PATCH  /api/blocks/{id}/  → atualiza (desativar bloqueio reativa o cartão)
    """
    queryset = Block.objects.select_related('user').all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BlockFilter
    search_fields = ['user__name', 'reason']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return BlockCreateSerializer
        return BlockSerializer
