import uuid

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
import random

from crm.models import AddressModel, AppUserModel, CustomerRelationshipModel
from shared.contract import Gender


class Command(BaseCommand):
    help = 'Help to generate fake data'

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
            help='Specifies the number of address records to create.'
        )

    def handle(self, *args, **options):
        fake = Faker()
        batch_size = options['batch']
        customer_num = options['customers']
        address_size = customer_num//2

        self.stdout.write(
            f'Generating {customer_num} customers and {address_size} addresses...'
        )

        with transaction.atomic():
            addresses = []
            for i in range(address_size):
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

            customers = []
            for i in range(customer_num):
                customer = AppUserModel(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    gender=random.choice(Gender.get_genders()),
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
            num_to_select = min(len(customer_ids), customer_num)
            selected_customers = random.sample(customer_ids, num_to_select)

            relationships = []
            for customer_id in selected_customers:
                activity_time = timezone.make_aware(fake.date_time_between(start_date='-3y'))

                relationships.append(CustomerRelationshipModel(
                    appuser_id=customer_id,
                    points=random.randint(0, 50_000),
                    last_activity=activity_time
                ))

                if len(relationships) >= batch_size:
                    CustomerRelationshipModel.objects.bulk_create(relationships, ignore_conflicts=True)
                    relationships = []

            if relationships:
                CustomerRelationshipModel.objects.bulk_create(relationships, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Data generation completed!'))