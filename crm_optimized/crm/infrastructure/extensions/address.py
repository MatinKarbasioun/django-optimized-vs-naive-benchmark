from crm.infrastructure.models import AddressModel
from crm.domain.entities import Address


class AddressToModel:
    def __rmatmul__(self, address: Address) -> AddressModel:
        return AddressModel(
            street=address.street,
            street_number=address.street_number,
            city_code=address.city_code,
            city=address.city,
            country=address.country
        )


class ModelToAddress:

    def __rmatmul__(self, address: AddressModel | None) -> Address | None:

        return Address(
            id=address.id,
            street=address.street,
            street_number=address.street_number,
            city_code=address.city_code,
            city=address.city,
            country=address.country
        ) if address else None
