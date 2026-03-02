from django_filters import rest_framework as filters
from core.models import User, TransportCard, Ride, TopUp, Block


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=User.STATUS_CHOICES)

    class Meta:
        model = User
        fields = ['name', 'email', 'status', 'active']


class TransportCardFilter(filters.FilterSet):
    card_number = filters.CharFilter(field_name='card_number', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=TransportCard.STATUS_CHOICES)
    balance_gte = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    balance_lte = filters.NumberFilter(field_name='balance', lookup_expr='lte')

    class Meta:
        model = TransportCard
        fields = ['status', 'active', 'user']


class RideFilter(filters.FilterSet):
    date_after = filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    date_before = filters.DateTimeFilter(field_name='date', lookup_expr='lte')
    fare_gte = filters.NumberFilter(field_name='fare', lookup_expr='gte')
    fare_lte = filters.NumberFilter(field_name='fare', lookup_expr='lte')

    class Meta:
        model = Ride
        fields = ['user', 'card', 'active']


class TopUpFilter(filters.FilterSet):
    date_after = filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    date_before = filters.DateTimeFilter(field_name='date', lookup_expr='lte')
    method = filters.ChoiceFilter(choices=TopUp.METHOD_CHOICES)
    amount_gte = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_lte = filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = TopUp
        fields = ['user', 'method', 'active']


class BlockFilter(filters.FilterSet):
    class Meta:
        model = Block
        fields = ['user', 'active']
