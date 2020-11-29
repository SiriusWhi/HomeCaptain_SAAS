from django.contrib import admin

from .models import (
    LoanOfficer,
    Lender,
)

admin.site.register(LoanOfficer)
admin.site.register(Lender)
