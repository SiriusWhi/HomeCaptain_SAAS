from decimal import Decimal
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.util.models import HomeCaptainAbstractBaseModel, Address
from apps.event.models import Event

DECIMAL_DEFAULT = Decimal()

class Service(HomeCaptainAbstractBaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return "{self.name}"
    
class ServiceProvider(HomeCaptainAbstractBaseModel):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255)
    address = models.OneToOneField(Address, on_delete=models.PROTECT, null=True)
    phone_number = PhoneNumberField(blank=True)
    #picture = models.ImageField(upload_to='media/uploads/customer_profile_pics',
    #                            blank=True)
    about = models.TextField()

    services = models.ManyToManyField(Service)
    
    def __str__(self):
        return "{self.first_name} ({self.uid})"


class ServiceRequest(HomeCaptainAbstractBaseModel):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    bill_amount = models.DecimalField(max_digits=8, decimal_places=2,
                                      default=DECIMAL_DEFAULT)

    is_service_complete = models.BooleanField(default=False)
    service_completion_date = models.DateField(null=True)
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    feedback = models.TextField()
    #invoice = models.ImageField()
    payment_link = models.URLField(max_length=512, blank=True)
    invoice_paid_date = models.DateField(null=True)


    def __str__(self):
        return "{self.event.property.id} {self.event.event_config.name}"
