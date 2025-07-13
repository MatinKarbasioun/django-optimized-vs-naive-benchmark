from crm.domain import Customer, Gender
from crm.infrastructure.extensions import ModelToAddress
from crm.infrastructure.models import AppUserModel


class CustomerToModel:
    def __rmatmul__(self, customer: Customer) -> AppUserModel:
        return AppUserModel(
            first_name=customer.first_name,
            last_name=customer.last_name,
            customer_id=customer.customer_id,
            birthday=customer.birthday,
            gender=customer.gender.value
        )


class ModelToCustomer:
    def __rmatmul__(self, model: AppUserModel | None) -> Customer | None:
        return Customer(
            id=model.id,
            customer_id=model.customer_id,
            first_name=model.first_name,
            last_name=model.last_name,
            birthday=model.birthday,
            address=model.address @ ModelToAddress(),
            gender=Gender(model.gender),
            created=model.created,
        ) if model else None