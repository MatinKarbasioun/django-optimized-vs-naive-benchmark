from crm.application.schemas.address import AddressSchema
from crm.domain.entities import Address


class SchemToAddress:
    def __rmatmul__(self, address: AddressSchema) -> Address:
        return Address(
            id=None,
            country=address.country,
            city=address.city,
            city_code=address.city_code,
            street=address.street,
        street_number=address.street_number
        )