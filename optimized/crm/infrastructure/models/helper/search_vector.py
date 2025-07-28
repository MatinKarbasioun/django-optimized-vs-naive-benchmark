from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models
from django.db.models import Value, ExpressionWrapper
from django.db.models.functions import Coalesce, Cast

text_field = models.TextField()

def generate_app_user_search_vector():
    def as_text(field_name):
        return Coalesce(Cast(field_name, text_field), Value(''), output_field=text_field)

    # Combine all vectors into a single expression
    vector_expression = (
        SearchVector(
            as_text('first_name'),
            as_text('last_name'),
            as_text('customer_id'),
            weight='A'
        ) +
        SearchVector(
            as_text('birthday'),
            as_text('phone_number'),
            as_text('address__city'),
            as_text('address__country'),
            weight='B'
        ) +
        SearchVector(
            as_text('address__street'),
            as_text('address__street_number'),
            as_text('address__city_code'),
            as_text('relationship__points'),
            weight='C'
        ) +
        SearchVector(
            as_text('relationship__created'),
            as_text('relationship__last_activity'),
            weight='D'
        )
    )

    # Wrap the final expression and define its output type for safety.
    return ExpressionWrapper(vector_expression, output_field=SearchVectorField())