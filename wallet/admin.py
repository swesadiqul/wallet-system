from django.contrib import admin
from wallet.models import *

# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = "Wallet System"
admin.site.site_title = "bdCalling IT Ltd"
admin.site.index_title = "Wallet System Administration"