from crm.application.query import Ordering


class ToPrefix:
    def __rmatmul__(self, ordering: Ordering):
        return "-" if ordering == Ordering.DESCENDING else ""