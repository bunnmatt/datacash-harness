from django.contrib import admin

from .models import Environment
from .models import Account
from .models import Pageset
from .models import Transaction

admin.site.register(Environment)
admin.site.register(Account)
admin.site.register(Pageset)
admin.site.register(Transaction)


