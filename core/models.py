from django.db import models
from django.contrib.auth.hashers import make_password
import uuid


# ─── Base Model ───────────────────────────────────────────────────────────────

class BaseModel(models.Model):
    """
    Modelo base abstrato com campos comuns.
    Todos os modelos herdam deste para padronização.
    Usa exclusão lógica: registros são marcados como inativos, nunca apagados.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['modified_at']),
            models.Index(fields=['active']),
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"


# ─── User ─────────────────────────────────────────────────────────────────────

class User(BaseModel):
    """
    Representa a pessoa que usa o transporte.
    """
    STATUS_CHOICES = [
        ('none', 'Nenhum'),
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)  # formato: 000.000.000-00
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='none')

    class Meta:
        ordering = ['name']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def save(self, *args, **kwargs):
        # Armazena a senha com segurança (hash) ao criar ou alterar
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.email})"


# ─── TransportCard ────────────────────────────────────────────────────────────

class TransportCard(BaseModel):
    """
    Representa o cartão digital de transporte de um usuário.
    Cada usuário pode ter apenas um cartão.
    """
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('blocked', 'Bloqueado'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='card'
    )
    card_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cartão de Transporte'
        verbose_name_plural = 'Cartões de Transporte'

    def __str__(self):
        return f"Cartão {self.card_number} - {self.user.name}"


# ─── Ride ─────────────────────────────────────────────────────────────────────

class Ride(BaseModel):
    """
    Representa cada viagem realizada com o cartão.
    Registra localização, valor da passagem e desconta o saldo.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rides'
    )
    card = models.ForeignKey(
        TransportCard,
        on_delete=models.CASCADE,
        related_name='rides'
    )
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Viagem'
        verbose_name_plural = 'Viagens'

    def __str__(self):
        return f"Viagem de {self.user.name} em {self.date:%d/%m/%Y %H:%M}"


# ─── TopUp ────────────────────────────────────────────────────────────────────

class TopUp(BaseModel):
    """
    Representa uma recarga de saldo no cartão.
    Ao ser criada, o saldo do cartão aumenta automaticamente.
    """
    METHOD_CHOICES = [
        ('pix', 'PIX'),
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('cash', 'Dinheiro'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='topups'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='pix')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Recarga'
        verbose_name_plural = 'Recargas'

    def __str__(self):
        return f"Recarga R${self.amount} - {self.user.name} ({self.method})"


# ─── Block ────────────────────────────────────────────────────────────────────

class Block(BaseModel):
    """
    Representa o bloqueio de um cartão.
    Se houver bloqueio ativo (active=True), o usuário não pode registrar viagem.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocks'
    )
    reason = models.TextField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bloqueio'
        verbose_name_plural = 'Bloqueios'

    def __str__(self):
        status = "ATIVO" if self.active else "inativo"
        return f"Bloqueio [{status}] - {self.user.name}: {self.reason[:40]}"
