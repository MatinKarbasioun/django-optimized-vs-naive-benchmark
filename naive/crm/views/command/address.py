from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAddressCommand:
    street: str
    street_number: str
    city_code: str
    city: str
    country: str