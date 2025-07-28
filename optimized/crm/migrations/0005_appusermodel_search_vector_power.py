from django.db import migrations

from crm.infrastructure.models.helper.search_vector import generate_app_user_search_vector


def update_search_vector(apps, schema_editor):
    AppUserModel = apps.get_model('crm', 'AppUserModel')

    # Annotate the queryset to calculate the vector, then iterate and update.
    # This is the correct pattern to work around the update() limitation.
    print("\nPopulating search vectors... (This may take a while on large datasets)")
    users_with_vector = AppUserModel.objects.annotate(new_vector=generate_app_user_search_vector())

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
