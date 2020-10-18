from rest_framework.permissions import BasePermission
from django.utils.timezone import now, localtime


class IsBookingOwner(BasePermission):
    message = "You must be the owner of this booking"

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or (obj.customer == request.user):
            return True
        else:
            return False


class IsChangable(BasePermission):
    message = "Booking cannot be cancelled or modified"

    def has_object_permission(self, request, view, obj):
        if obj.class_of.start > localtime():
            return True
        else:
            return False
