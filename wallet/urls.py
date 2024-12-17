from django.urls import path
from wallet.views import *


urlpatterns = [
    path('api/wallet/', WalletView.as_view(), name='wallet'),
    path('', index,)
]