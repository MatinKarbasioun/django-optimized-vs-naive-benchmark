from django.db import migrations

from crm.infrastructure.models.helper.search_vector import generate_app_user_search_vector


def update_search_vector(apps, schema_editor):
    AppUserModel = apps.get_model('crm', 'AppUserModel')

    print("\nPopulating search vectors... (This may take a while on large datasets)")
    users_with_vector = AppUserModel.objects.annotate(new_vector=generate_app_user_search_vector())

    for user in users_with_vector.iterator(chunk_size=10000):
        AppUserModel.objects.filter(pk=user.pk).update(search_vector=user.new_vector)

    print("Search vector population complete.")


class Migration(migrations.Migration):
    dependencies = [
        ('crm', '0008_alter_addressmodel_city_alter_addressmodel_city_code_and_more'),
    ]
    operations = [
        migrations.RunPython(update_search_vector, reverse_code=migrations.RunPython.noop),
    ]
