import uuid
import random
import asyncio

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from asgiref.sync import sync_to_async

from crm.infrastructure.models import AddressModel, AppUserModel, CustomerRelationshipModel


class Command(BaseCommand):
    help = 'Generate 3M test records asynchronously'

    async def handle(self, *args, **options):
        fake = Faker()
        batch_size = 10000

        self.stdout.write('Generating test data...')

        # Use sync_to_async for the transaction context manager
        # Django's atomic block is not yet async-native.
        atomic_transaction = sync_to_async(transaction.atomic, thread_sensitive=True)

        async with atomic_transaction():
            # Generate addresses
            addresses = []
            for i in range(100000):
                addresses.append(AddressModel(
                    street=fake.street_name(),
                    street_number=str(fake.building_number()),
                    city_code=fake.postcode(),
                    city=fake.city(),
                    country=fake.country()
                ))

                if len(addresses) >= batch_size:
                    await AddressModel.objects.abulk_create(addresses)
                    addresses = []
                    self.stdout.write(f'Created {i + 1} addresses')

            if addresses:
                await AddressModel.objects.abulk_create(addresses)

            # Asynchronously get all address IDs
            address_ids = [pk async for pk in AddressModel.objects.values_list('id', flat=True)]

            # Generate customers
            customers = []
            for i in range(3000000):
                customers.append(AppUserModel(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    gender=random.choice(['M', 'F', 'O']),
                    customer_id=uuid.uuid4().hex,
                    phone_number=fake.phone_number()[:20],
                    birthday=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    address_id=random.choice(address_ids) if random.random() > 0.1 else None
                ))

                if len(customers) >= batch_size:
                    await AppUserModel.objects.abulk_create(customers)
                    customers = []
                    self.stdout.write(f'Created {i + 1} customers')

            if customers:
                await AppUserModel.objects.abulk_create(customers)

            # Generate relationships
            customer_ids_qs = AppUserModel.objects.values_list('id', flat=True)
            customer_ids = [pk async for pk in customer_ids_qs]

            # Note: random.sample is synchronous. For very large lists, consider alternatives if this becomes a bottleneck.
            selected_customers = random.sample(customer_ids, 2500000)

            relationships = []
            for customer_id in selected_customers:
                relationships.append(CustomerRelationshipModel(
                    appuser_id=customer_id,
                    points=random.randint(0, 50000),
                    last_activity=fake.date_time_between(start_date='-2y') if random.random() > 0.2 else None
                ))

                if len(relationships) >= batch_size:
                    await CustomerRelationshipModel.objects.abulk_create(relationships, ignore_conflicts=True)
                    relationships = []

            if relationships:
                await CustomerRelationshipModel.objects.abulk_create(relationships, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Data generation completed!'))