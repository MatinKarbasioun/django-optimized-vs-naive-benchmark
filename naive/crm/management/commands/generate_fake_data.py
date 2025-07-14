import uuid

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random

from crm.infrastructure.models import AddressModel, AppUserModel, CustomerRelationshipModel


class Command(BaseCommand):
    help = 'Help to generate fake data'

    def handle(self, *args, **options):
        fake = Faker()
        batch_size = 10000

        self.stdout.write('Generating test data...')

        with transaction.atomic():
            # Generate addresses
            addresses = []
            for i in range(100000):
                address = AddressModel(
                    street=fake.street_name(),
                    street_number=str(fake.building_number()),
                    city_code=fake.postcode(),
                    city=fake.city(),
                    country=fake.country()
                )
                addresses.append(address)

                if len(addresses) >= batch_size:
                    AddressModel.objects.bulk_create(addresses)
                    addresses = []
                    self.stdout.write(f'Created {i + 1} addresses')

            if addresses:
                AddressModel.objects.bulk_create(addresses)

            address_ids = list(AddressModel.objects.values_list('id', flat=True))

            # Generate customers
            customers = []
            for i in range(3000000):
                customer = AppUserModel(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    gender=random.choice(['M', 'F', 'O']),
                    customer_id=uuid.uuid4().hex,
                    phone_number=fake.phone_number()[:20],
                    birthday=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    address_id=random.choice(address_ids) if random.random() > 0.1 else None
                )
                customers.append(customer)

                if len(customers) >= batch_size:
                    AppUserModel.objects.bulk_create(customers)
                    customers = []
                    self.stdout.write(f'Created {i + 1} customers')

            if customers:
                AppUserModel.objects.bulk_create(customers)

            # Generate relationships
            customer_ids = list(AppUserModel.objects.values_list('id', flat=True))
            selected_customers = random.sample(customer_ids, 2500000)

            relationships = []
            for customer_id in selected_customers:
                relationship = CustomerRelationshipModel(
                    appuser_id=customer_id,
                    points=random.randint(0, 50000),
                    last_activity=fake.date_time_between(start_date='-2y') if random.random() > 0.2 else None
                )
                relationships.append(relationship)

                if len(relationships) >= batch_size:
                    CustomerRelationshipModel.objects.bulk_create(relationships, ignore_conflicts=True)
                    relationships = []

            if relationships:
                CustomerRelationshipModel.objects.bulk_create(relationships, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Data generation completed!'))