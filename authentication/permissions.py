from rest_framework import permissions


class IsUnauthenticatedOrCannotPostUser(permissions.BasePermission):


    def has_permission(self, request, view):

        if request.method == "POST":

            return not request.user.is_authenticated

        return True



class IsStaffOrPostOnly(permissions.BasePermission):

    def has_permission(self, request, view):
    
        if not request.user.is_staff:

            return request.method == "POST"

        return True