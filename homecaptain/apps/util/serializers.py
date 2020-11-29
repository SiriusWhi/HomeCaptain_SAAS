from rest_framework import serializers
from rest_framework.fields import empty

from django.db.models import FieldDoesNotExist

from apps.util.models import DECIMAL_DEFAULT
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'uid', 'street', 'city', 'state', 'postalcode', 'country')

class HCWritableNestedModelSerializer(serializers.ModelSerializer): 
    """
    A base WritableNestedModelSerializer where we can plug in common code is required

    #https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    A ModelSerializer that takes additional `exclude` and/or `fields` arguments that
    controls which fields should be displayed. `exclude` takes priority, if both are given
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        
        # Instantiate the superclass normally
        super(HCWritableNestedModelSerializer, self).__init__(*args, **kwargs)

        #exclude take priority
        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)
        elif fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
