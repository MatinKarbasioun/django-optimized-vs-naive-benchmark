import uuid
import random
import asyncio

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
from asgiref.sync import sync_to_async

from crm.infrastructure.models import AddressModel, AppUserModel, CustomerRelationshipModel


class Command(BaseCommand):
    help = 'Help to generate fake data asynchronously'

    def add_arguments(self, parser):
        parser.add_argument(
            '--customers',
            type=int,
            default=1000,
            help='Specifies the number of customer records to create.'
        )
        parser.add_argument(
            '--batch',
            type=int,
            default=50_000,
            help='Specifies the batch size for bulk inserts.'
        )

    async def handle(self, *args, **options):
        fake = Faker()
        batch_size = options['batch']
        customer_num = options['customers']
        address_size = customer_num // 2

        self.stdout.write(
            f'Generating {customer_num} customers and {address_size} addresses...'
        )

        # Make the transaction context manager async-compatible
        atomic_transaction = sync_to_async(transaction.atomic, thread_sensitive=True)

        async with atomic_transaction():
            # Generate addresses
            addresses = []
            for i in range(address_size):
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

            # Asynchronously fetch IDs
            address_ids = [pk async for pk in AddressModel.objects.values_list('id', flat=True)]

            # Generate customers
            customers = []
            for i in range(customer_num):
                customers.append(AppUserModel(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    gender=random.choice(['M', 'F', 'O']),
                    customer_id=uuid.uuid4().hex,
                    phone_number=fake.phone_number()[:20],
                    birthday=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    address_id=random.choice(address_ids) if random.random() > 0.1 and address_ids else None
                ))

                if len(customers) >= batch_size:
                    await AppUserModel.objects.abulk_create(customers)
                    customers = []
                    self.stdout.write(f'Created {i + 1} customers')

            if customers:
                await AppUserModel.objects.abulk_create(customers)

            # Generate relationships
            customer_ids = [pk async for pk in AppUserModel.objects.values_list('id', flat=True)]
            num_to_select = min(len(customer_ids), customer_num)
            selected_customers = random.sample(customer_ids, num_to_select)

            relationships = []
            for customer_id in selected_customers:
                activity_time = timezone.make_aware(
                    fake.date_time_between(start_date='-3y')) if random.random() > 0.2 else None

                relationships.append(CustomerRelationshipModel(
                    appuser_id=customer_id,
                    points=random.randint(0, 50_000),
                    last_activity=activity_time
                ))

                if len(relationships) >= batch_size:
                    await CustomerRelationshipModel.objects.abulk_create(relationships, ignore_conflicts=True)
                    relationships = []

            if relationships:
                await CustomerRelationshipModel.objects.abulk_create(relationships, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Data generation completed!'))