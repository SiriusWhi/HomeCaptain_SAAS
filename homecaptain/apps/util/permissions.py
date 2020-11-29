from rest_framework import permissions
from apps.event.models import Event
from apps.property.models import Property

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
        
class IsRealtor(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (hasattr(request.user, 'realtor') and \
                getattr(request.user, 'realtor', None)) or request.user.is_staff
            
    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'create', 'list', 'recommend', 'archive', 'restore',
                           'unarchive', 'update', 'partial_update', 'status_update', 'add_recommend']:
            if request.user.is_staff:
                return True
            ##FIXME: when the same customer is both a buyer and seller,
            ##we will have to modify this
            if hasattr(obj, 'requirements') and obj.requirements.count():
                return obj.requirements.filter(
                    realtor__user=request.user).exists()
            ##FIXME: Just allowing all properties for the realtor,
            ## we will have to modify this according to the property, buyers and sellers
            if isinstance(obj, Property):
                return True
            # FIXME: Just allowing all events for the realtor,
            # we will have to modify this according to the events
            if isinstance(obj, Event):
                return True
            elif hasattr(obj, 'requirement_set') and obj.requirement_set.count():
                return obj.requirement_set.filter(
                    realtor__user=request.user).exists()
            #elif hasattr(obj, 'customer') and getattr(obj, 'customer', None):
                
            elif hasattr(obj, 'properties') and obj.properties.count():
                return obj.properties.filter(realtor__user=request.user).exists()
            elif hasattr(obj, 'property') and getattr(obj, 'property', None):
                return obj.property.realtor.user == request.user
            else:
                return obj.realtor.user==request.user
        return False

class IsLoanOfficer(permissions.BasePermission):

    def has_permission(self, request, view):
        return (hasattr(request.user, 'loan_officer') and
                getattr(request.user, 'loan_officer', None)) or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'create', 'list', 'recommend', 'archive', 'restore', 'discourage',
                           'unarchive', 'update', 'partial_update', 'status_update', 'add_recommend']:
            if request.user.is_staff:
                return True
            # FIXME: when the same customer is both a buyer and seller,
            # we will have to modify this
            if hasattr(obj, 'requirements') and obj.requirements.count():
                return obj.requirements.filter(
                    loan_officer__user=request.user).exists()
            # FIXME: Just allowing all properties for the realtor,
            # we will have to modify this according to the property, buyers and sellers
            if isinstance(obj, Property):
                return True
            # FIXME: Just allowing all events for the realtor,
            # we will have to modify this according to the events
            if isinstance(obj, Event):
                return True
            elif hasattr(obj, 'requirement_set') and obj.requirement_set.count():
                return obj.requirement_set.filter(
                    loan_officer__user=request.user).exists()
            # elif hasattr(obj, 'customer') and getattr(obj, 'customer', None):

            elif hasattr(obj, 'properties') and obj.properties.count():
                return obj.properties.filter(loan_officer__user=request.user).exists()
            elif hasattr(obj, 'property') and getattr(obj, 'property', None):
                return obj.property.loan_officer.user == request.user
            else:
                return obj.loan_officer.user == request.user
        return False

class IsCustomer(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (hasattr(request.user, 'customer') and
                getattr(request.user, 'customer', None)) or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'create', 'list', 'recommend', 'archive', 'restore', 'discourage',
                           'unarchive', 'update', 'partial_update', 'status_update', 'add_recommend']:
            if request.user.is_staff:
                return True
            # FIXME: when the same customer is both a buyer and seller,
            # we will have to modify this
            if hasattr(obj, 'requirements') and obj.requirements.count():
                return obj.requirements.filter(
                    customer__user=request.user).exists()
            # FIXME: Just allowing all properties for the realtor,
            # we will have to modify this according to the property, buyers and sellers
            if isinstance(obj, Property):
                return True
            # FIXME: Just allowing all events for the realtor,
            # we will have to modify this according to the events
            if isinstance(obj, Event):
                return True
            elif hasattr(obj, 'requirement_set') and obj.requirement_set.count():
                return obj.requirement_set.filter(
                    customer__user=request.user).exists()
            # elif hasattr(obj, 'customer') and getattr(obj, 'customer', None):

            elif hasattr(obj, 'properties') and obj.properties.count():
                return obj.properties.filter(customer__user=request.user).exists()
            elif hasattr(obj, 'property') and getattr(obj, 'property', None):
                return obj.property.customer.user == request.user
            else:
                return obj.customer.user == request.user
        return False
