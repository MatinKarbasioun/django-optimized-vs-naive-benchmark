from django.contrib.postgres.search import SearchVector
from django.db import migrations, models
from django.db.models import Value
from django.db.models.functions import Cast, Coalesce


def update_search_vector(apps, schema_editor):
    AppUserModel = apps.get_model('crm', 'AppUserModel')

    vector = (
            SearchVector('first_name', weight='A') +
            SearchVector('last_name', weight='A') +
            SearchVector(Coalesce('customer_id', Value('')), weight='B') +
            SearchVector(Coalesce('phone_number', Value('')), weight='C') +
            SearchVector(Coalesce('address__street', Value('')), weight='D') +
            SearchVector(Coalesce('address__city', Value('')), weight='C') +
            SearchVector(Coalesce('address__country', Value('')), weight='C') +
            SearchVector(Coalesce('address__street_number', Value('')), weight='D') +
            SearchVector(
                Cast(Coalesce('relationship__points', Value(0)), models.TextField()),
                weight='D'
            ) +
            SearchVector(
                Cast(Coalesce('relationship__last_activity', Value(None)), models.TextField()),
                weight='D'
            )
    )

    # Annotate the queryset to calculate the vector, then iterate and update.
    # This is the correct pattern to work around the update() limitation.
    print("\nPopulating search vectors... (This may take a while on large datasets)")
    users_with_vector = AppUserModel.objects.annotate(new_vector=vector)

    # Process in batches for memory efficiency
    for user in users_with_vector.iterator(chunk_size=2000):
        AppUserModel.objects.filter(pk=user.pk).update(search_vector=user.new_vector)

    print("Search vector population complete.")


class Migration(migrations.Migration):
    dependencies = [
        ('crm', '0004_appusermodel_search_vector_and_more'),
    ]
    operations = [
        migrations.RunPython(update_search_vector, reverse_code=migrations.RunPython.noop),
    ]
