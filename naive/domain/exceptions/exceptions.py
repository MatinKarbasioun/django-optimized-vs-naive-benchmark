class DomainException(Exception):
    """Base domain exception"""
    pass

class CustomerNotFoundError(DomainException):
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        super().__init__(f"Customer with ID {customer_id} not found")


class CustomerExistException(DomainException):
    pass


class CustomerInvalidDataException(DomainException):
    pass