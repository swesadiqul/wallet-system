from django.urls import path
from wallet.views import *


urlpatterns = [
    path('', index),
    path('api/wallet/', WalletView.as_view(), name='wallet')
]