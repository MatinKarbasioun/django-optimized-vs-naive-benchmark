from rest_framework.generics import ListAPIView
from rest_framework import filters


class User(ListAPIView):

    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'email', 'last_name', 'gender', 'created', 'address']

    def get_user(self, request):
        pass
