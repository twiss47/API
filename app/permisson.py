from rest_framework.permissions import BasePermission, SAFE_METHODS
from datetime import datetime, timedelta
from django.utils import timezone



class UpdateInLimitedTime(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return True
        return True
    
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method in ('PUT','PATCH','DELETE'):
            now = timezone.localtime()
            allow_until = obj.created_at + timedelta(hours=4)


            return now <= allow_until
        
        return False



















#monday-froday is allowed
# class DayTimePermission(BasePermission):

#     def has_permission(self, request, view):
#         now = timezone.localtime()

#         weekday = datetime.weekday()
#         current_time = now.time()

#         start_time = (9,0)
#         end_time = (21,0)

#         is_weekday =  weekday <= 4
#         is_time_ok = start_time <= current_time <= end_time

#         return is_weekday and is_time_ok
    




# class TwisBlocket(BasePermission):
    
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
        

#         if request.method in ('PUT','PATCH','DELETE'):
#             user = request.user

#             if user and user.is_authenticated and user.username == "twis":
#                 return False
#         return True




