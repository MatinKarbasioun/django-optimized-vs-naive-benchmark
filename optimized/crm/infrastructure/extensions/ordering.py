from crm.application.schemas.sorting import Ordering


class ToPrefix:
    def __rmatmul__(self, ordering: Ordering):
        return "-" if ordering == Ordering.DESCENDING else ""