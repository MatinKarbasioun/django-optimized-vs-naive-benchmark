import asyncio
import uuid
import random
from faker import Faker

from django.core.management.base import BaseCommand
from django.utils import timezone

from crm.domain.value_objects import Gender
from crm.infrastructure.models import AddressModel, AppUserModel, CustomerRelationshipModel
from shared.utils import AsyncAtomicContextManager


class Command(BaseCommand):
    help = 'Generates fake data'

    def add_arguments(self, parser):
        parser.add_argument('--customers', type=int, default=1000, help='Number of customers to create.')
        parser.add_argument('--batch', type=int, default=1000, help='Batch size for bulk inserts.')

    async def _create_addresses(self, ctx_manager: AsyncAtomicContextManager, fake: Faker, count: int, batch_size: int):
        self.stdout.write(f"Generating {count} addresses")
        addresses_to_create = []
        for i in range(count):
            addresses_to_create.append(AddressModel(
                street=fake.street_name(), street_number=str(fake.building_number()),
                city_code=fake.postcode(), city=fake.city(), country=fake.country()
            ))
            if len(addresses_to_create) >= batch_size:
                await ctx_manager.run_in_context(AddressModel.objects.bulk_create, addresses_to_create)
                self.stdout.write(f"created {i + 1}/{count} addresses")
                addresses_to_create = []
        if addresses_to_create:
            await ctx_manager.run_in_context(AddressModel.objects.bulk_create, addresses_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} addresses"))
        return await ctx_manager.run_in_context(list, AddressModel.objects.values_list('id', flat=True))

    async def _create_customers(self, ctx_manager: AsyncAtomicContextManager, fake: Faker, count: int, batch_size: int, address_ids: list):
        self.stdout.write(f"Generating {count} customers")
        customers_to_create = []
        for i in range(count):
            customers_to_create.append(AppUserModel(
                first_name=fake.first_name(), last_name=fake.last_name(), gender=random.choice(Gender.get_genders()),
                customer_id=uuid.uuid4().hex, phone_number=fake.phone_number()[:32],
                birthday=fake.date_of_birth(minimum_age=18, maximum_age=80),
                address_id=random.choice(address_ids) if random.random() > 0.1 and address_ids else None
            ))
            if len(customers_to_create) >= batch_size:
                await ctx_manager.run_in_context(AppUserModel.objects.bulk_create, customers_to_create)
                self.stdout.write(f"created {i + 1}/{count} customers")
                customers_to_create = []
        if customers_to_create:
            await ctx_manager.run_in_context(AppUserModel.objects.bulk_create, customers_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} customers."))
        return await ctx_manager.run_in_context(list, AppUserModel.objects.values_list('id', flat=True))

    async def _create_relationships(self, ctx_manager: AsyncAtomicContextManager, fake: Faker, count: int, batch_size: int, customer_ids: list):
        self.stdout.write(f"--- Generating {count} relationships ---")
        num_to_select = min(len(customer_ids), count)
        selected_customer_ids = random.sample(customer_ids, num_to_select)
        relationships_to_create = []
        for i, customer_id in enumerate(selected_customer_ids):
            activity_time = timezone.make_aware(fake.date_time_between(start_date='-3y')) if random.random() > 0.2 else None
            relationships_to_create.append(CustomerRelationshipModel(
                appuser_id=customer_id, points=random.randint(0, 50_000), last_activity=activity_time
            ))
            if len(relationships_to_create) >= batch_size:
                await ctx_manager.run_in_context(CustomerRelationshipModel.objects.bulk_create, relationships_to_create, ignore_conflicts=True)
                self.stdout.write(f"  ...created {i + 1}/{count} relationships")
                relationships_to_create = []
        if relationships_to_create:
            await ctx_manager.run_in_context(CustomerRelationshipModel.objects.bulk_create, relationships_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_to_select} relationships."))

    def handle(self, *args, **options):
        asyncio.run(self.a_handle(*args, **options))

    async def a_handle(self, *args, **options):
        fake = Faker()
        batch_size = options['batch']
        customer_num = options['customers']
        address_num = customer_num // 2

        self.stdout.write(self.style.SUCCESS(f'Starting data generation for {customer_num} customers...'))

        async with AsyncAtomicContextManager() as ctx_manager:
            address_ids = await self._create_addresses(ctx_manager, fake, address_num, batch_size)
            customer_ids = await self._create_customers(ctx_manager, fake, customer_num, batch_size, address_ids)
            await self._create_relationships(ctx_manager, fake, customer_num, batch_size, customer_ids)

        self.stdout.write(self.style.SUCCESS('Data generation completed successfully!'))