from application.command import CreateAddressCommand
from domain import Address


class CommandToAddress:

    def __rmatmul__(self, command: CreateAddressCommand) -> Address:
        return Address(
                id=None,
                street=command.street,
                street_number=command.street_number,
                city_code=command.city_code,
                city=command.city,
                country=command.country
            )