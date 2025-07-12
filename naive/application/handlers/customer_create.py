import logging

from kink import inject
from django.db import transaction
from django.db.utils import IntegrityError

from application.command import CreateCustomerCommand
from domain import Customer, CustomerRelationship
from domain.exceptions import CustomerExistException
from domain.exceptions.exceptions import CustomerInvalidDataException
from domain.repositories import ICustomerRepository, ICustomerRelationshipRepository, IAddressRepository
from shared.extensions import CommandToCustomer, CommandToAddress

logger = logging.getLogger(__name__)


@inject
class CustomerCreationHandler:

    def __init__(
            self,
            customer_repository: ICustomerRepository,
            address_repository: IAddressRepository,
            relationship_repository: ICustomerRelationshipRepository
    ):
        self._customer_repository = customer_repository
        self._address_repository = address_repository
        self._relationship_repository = relationship_repository

    @transaction.atomic
    def handle(self, command: CreateCustomerCommand) -> Customer:
        try:
            self._validate_business_rules(command)

            address = command.address @ CommandToAddress()
            self._address_repository.add(address)

            logger.debug(f"address created with ID: {address.id}")

            customer = command @ CommandToCustomer(address)
            self._customer_repository.add(customer)

            logger.debug(f"Customer relationship created with ID: {customer.id}")

            customer_relationship = CustomerRelationship.create(command.initial_points)
            self._customer_repository.add(customer_relationship)

            logger.debug(f"Customer relationship created with ID: {customer_relationship.id}")

            return customer

        except IntegrityError as e:
            logger.error(f"create customer raised IntegrityError with detail: {e}")
            raise CustomerInvalidDataException(f"Customer creation failed due to data constraint violation: {e}")

        except Exception as e:
            logger.error(f"create customer raised error with detail: {e}")
            raise CustomerInvalidDataException(f"Customer creation failed due to error: {e}")

    def _validate_business_rules(self, command: CreateCustomerCommand):
        if self._customer_repository.is_exist(command.customer_id):
            raise CustomerExistException(f"Customer ID {command.customer_id} already exists")
