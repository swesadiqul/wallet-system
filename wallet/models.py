from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        ordering = ['-created_at']

    def get_balance(self):
        return self.balance

    def add_money(self, amount):
        if amount <= 0:
            raise ValidationError("Amount to add must be greater than zero.")
        self.balance += amount
        self.save()
        Transaction.objects.create(wallet=self, transaction_type='credit', amount=amount)

    def spend_money(self, amount):
        if amount <= 0:
            raise ValidationError("Amount to spend must be greater than zero.")
        if self.balance < amount:
            raise ValidationError("Insufficient balance.")
        self.balance -= amount
        self.save()
        Transaction.objects.create(wallet=self, transaction_type='debit', amount=amount)

    def __str__(self):
        return f"{self.user.phone}'s Wallet"
    

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'), 
        ('debit', 'Debit')
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount}"
