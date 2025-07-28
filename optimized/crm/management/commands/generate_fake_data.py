import asyncio
import uuid
import random
import time
from typing import List
from dataclasses import dataclass

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db import connection

from crm.domain.value_objects import Gender
from crm.infrastructure.models import AddressModel, AppUserModel, CustomerRelationshipModel


@dataclass
class GenerationConfig:
    customers: int = 10_000
    batch_size: int = 50_000
    address_ratio: float = 0.3
    search_vector_batch: int = 5_000
    max_workers: int = 4


class DataGenerator:
    def __init__(self, config: GenerationConfig):
        self.config = config
        self._init_data_pools()

    def _init_data_pools(self):
        from faker import Faker
        fake = Faker()

        pool_size = min(50_000, self.config.customers // 10)

        self.first_names = [fake.first_name() for _ in range(pool_size)]
        self.last_names = [fake.last_name() for _ in range(pool_size)]
        self.streets = [fake.street_name() for _ in range(pool_size // 10)]
        self.cities = [fake.city() for _ in range(pool_size // 20)]
        self.countries = [fake.country() for _ in range(100)]
        self.phone_prefixes = ['+43', '+49', '+33', '+39', '+34']
        self.genders = Gender.get_genders()

    def generate_address_batch(self, count: int) -> List[AddressModel]:
        addresses = []
        for _ in range(count):
            addresses.append(AddressModel(
                street=random.choice(self.streets),
                street_number=str(random.randint(1, 999)),
                city_code=f"{random.randint(1000, 9999)}",
                city=random.choice(self.cities),
                country=random.choice(self.countries)
            ))
        return addresses

    def generate_customer_batch(self, count: int, address_ids: List[int]) -> List[AppUserModel]:
        customers = []
        for _ in range(count):

            address_id = None
            if address_ids and random.random() < self.config.address_ratio:
                address_id = random.choice(address_ids)

            customers.append(AppUserModel(
                first_name=random.choice(self.first_names),
                last_name=random.choice(self.last_names),
                gender=random.choice(self.genders),
                customer_id=uuid.uuid4().hex,
                phone_number=f"{random.choice(self.phone_prefixes)}{random.randint(100_000_000, 999_999_999)}"[:32],
                birthday=timezone.now().date().replace(
                    year=random.randint(1_940, 2_005),
                    month=random.randint(1, 12),
                    day=random.randint(1, 28)
                ),
                address_id=address_id
            ))
        return customers

    def generate_relationship_batch(self, customer_ids: List[int]) -> List[CustomerRelationshipModel]:
        relationships = []
        for customer_id in customer_ids:
            activity_time = None
            if random.random() > 0.2:  # 80% have activity
                days_ago = random.randint(1, 1095)
                activity_time = timezone.now() - timedelta(days=days_ago)
                points = random.randint(0, 50_000)
            else:
                points = 0

            relationships.append(CustomerRelationshipModel(
                appuser_id=customer_id,
                points=points,
                last_activity=activity_time
            ))
        return relationships


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--customers', type=int, default=10_000, help='Number of Customers Data')
        parser.add_argument('--batch', type=int, default=10_000, help='Batch size')
        parser.add_argument('--skip-search', action='store_true', help='Do not generate search vector')
        parser.add_argument('--workers', type=int, default=4, help='Parallel Workers Num')

    def handle(self, *args, **options):
        start_time = time.time()

        config = GenerationConfig(
            customers=options['customers'],
            batch_size=options['batch'],
            max_workers=options['workers']
        )

        self.stdout.write(
            self.style.SUCCESS(f'Starting generation of {config.customers:,} customers')
        )

        # Use the PostgreSQL command to disable FK checks
        with connection.cursor() as cursor:
            self.stdout.write("Disabling foreign key checks (PostgreSQL method)...")
            cursor.execute("SET session_replication_role = 'replica';")

        try:
            asyncio.run(self._generate_data(config, options['skip_search']))

        finally:
            # Use the PostgreSQL command to re-enable FK checks
            with connection.cursor() as cursor:
                self.stdout.write("Re-enabling foreign key checks...")
                cursor.execute("SET session_replication_role = 'origin';")

        elapsed = time.time() - start_time
        rate = config.customers / elapsed
        self.stdout.write(
            self.style.SUCCESS(
                f'Generation completed in {elapsed:.2f}s ({rate:.0f} records/sec)'
            )
        )

    async def _generate_data(self, config: GenerationConfig, skip_search: bool):
        generator = DataGenerator(config)

        address_count = int(config.customers * config.address_ratio * 1.2)  # 20% buffer
        address_ids = await self._create_addresses(generator, address_count, config.batch_size)

        customer_ids = await self._create_customers(
            generator, config.customers, config.batch_size, address_ids
        )

        await self._create_relationships(
            generator, customer_ids, config.batch_size
        )

        if not skip_search:
            await self._update_search_vectors(config.search_vector_batch)

    async def _create_addresses(self, generator: DataGenerator, count: int, batch_size: int) -> List[int]:
        self.stdout.write(f"Creating {count:,} addresses")

        address_ids = []
        for batch_start in range(0, count, batch_size):
            batch_count = min(batch_size, count - batch_start)
            addresses_to_create = generator.generate_address_batch(batch_count)

            created_addresses = await AddressModel.objects.abulk_create(
                addresses_to_create, ignore_conflicts=True, batch_size=batch_size
            )

            if addresses_to_create:
                last_id = await AddressModel.objects.alatest('id')
                new_ids = await asyncio.to_thread(
                    list,
                    AddressModel.objects.filter(
                        id__lte=last_id.id,
                        id__gt=last_id.id - len(addresses_to_create)).values_list('id', flat=True)
                )
                address_ids.extend(new_ids)

            if (batch_start // batch_size + 1) % 5 == 0:
                self.stdout.write(f"  Processed {batch_start + batch_count:,}/{count:,} potential addresses")

        self.stdout.write(self.style.SUCCESS(f"Finished creating addresses, found {len(address_ids):,} IDs."))
        return address_ids

    async def _create_customers(self, generator: DataGenerator, count: int,
                                batch_size: int, address_ids: List[int]) -> List[int]:
        self.stdout.write(f"Creating {count:,} customers...")

        all_customer_ids = []
        for batch_start in range(0, count, batch_size):
            batch_count = min(batch_size, count - batch_start)
            customers_to_create = generator.generate_customer_batch(batch_count, address_ids)

            # Use native async bulk_create
            created_customers = await AppUserModel.objects.abulk_create(
                customers_to_create, ignore_conflicts=True, batch_size=batch_size
            )

            # abulk_create returns the created objects, allowing us to get their IDs.
            if created_customers:
                customer_ids = [customer.id for customer in created_customers if customer.id is not None]
                all_customer_ids.extend(customer_ids)

            if (batch_start // batch_size + 1) % 5 == 0:
                self.stdout.write(f"  Created {len(all_customer_ids):,}/{count:,} customers")


        self.stdout.write("Verifying all created customer IDs...")
        all_customer_ids = [pk async for pk in AppUserModel.objects.values_list('id', flat=True)]

        self.stdout.write(self.style.SUCCESS(f"Created and verified {len(all_customer_ids):,} customers"))
        return all_customer_ids

    async def _create_relationships(self, generator: DataGenerator,
                                    customer_ids: List[int], batch_size: int):
        self.stdout.write(f"Creating relationships for {len(customer_ids):,} customers...")
        created_count = 0

        for batch_start in range(0, len(customer_ids), batch_size):
            batch_ids = customer_ids[batch_start:batch_start + batch_size]
            relationships_to_create = generator.generate_relationship_batch(batch_ids)

            if relationships_to_create:

                await CustomerRelationshipModel.objects.abulk_create(
                    relationships_to_create, ignore_conflicts=True, batch_size=len(relationships_to_create)
                )
                created_count += len(relationships_to_create)

            if (batch_start // batch_size + 1) % 5 == 0:
                self.stdout.write(f"  Created {created_count:,} relationships")

        self.stdout.write(self.style.SUCCESS(f"Created {created_count:,} relationships"))

    async def _update_search_vectors(self, batch_size: int):
        self.stdout.write("Updating search vectors using an async cursor")

        def db_update():
            with connection.cursor() as cursor:
                cursor.execute("""
                     UPDATE app_user
                     SET search_vector = (
                         setweight(to_tsvector('english', COALESCE(app_user.first_name, '')), 'A') ||
                         setweight(to_tsvector('english', COALESCE(app_user.last_name, '')), 'A') ||
                         setweight(to_tsvector('simple', COALESCE(app_user.customer_id, '')), 'B') ||
                         setweight(to_tsvector('simple', COALESCE(app_user.phone_number, '')), 'C') ||
                         setweight(to_tsvector('english', COALESCE(a.street, '')), 'D') ||
                         setweight(to_tsvector('english', COALESCE(a.city, '')), 'C') ||
                         setweight(to_tsvector('english', COALESCE(a.country, '')), 'C') ||
                         setweight(to_tsvector('simple', COALESCE(a.street_number, '')), 'D') ||
                         setweight(to_tsvector('simple', COALESCE(r.points::text, '')), 'D') ||
                         setweight(to_tsvector('simple', COALESCE(r.last_activity::text, '')), 'D')
                         )
                     FROM app_user AS u 
                     LEFT JOIN address AS a ON u.address_id = a.id
                     LEFT JOIN customer_relationship AS r ON u.id = r.appuser_id
                     WHERE app_user.id = u.id
                     AND app_user.search_vector IS NULL;
                     """
                )

                return cursor.rowcount

        updated_count = await sync_to_async(db_update)()

        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count:,} search vectors"))