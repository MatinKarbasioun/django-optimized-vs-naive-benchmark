from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Value
from django.db.models.functions import Coalesce, Cast


def generate_app_user_search_vector():
    return(
                SearchVector('first_name', weight='A') +
                SearchVector('last_name', weight='A') +
                SearchVector(Coalesce('customer_id', Value('')), weight='B') +
                SearchVector(Coalesce('phone_number', Value('')), weight='C') +
                SearchVector(Coalesce('address__street', Value('')), weight='D') +
                SearchVector(Coalesce('address__city', Value('')), weight='C') +
                SearchVector(Coalesce('address__country', Value('')), weight='C') +
                SearchVector(Coalesce('address__street_number', Value('')), weight='D') +
                SearchVector(
                    Cast(Coalesce('relationship__points', Value(0)), models.TextField()), weight='D'
                ) +
                SearchVector(
                    Cast(Coalesce('relationship__created', Value(None)), models.TextField()), weight='D'
                ) +
                SearchVector(
                    Cast(Coalesce('relationship__last_activity', Value(None)), models.TextField()), weight='D'
                )
        )