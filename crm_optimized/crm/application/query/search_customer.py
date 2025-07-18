from typing import NamedTuple
from django.db.models import Q

from crm.application.query.sorting import Sorting


class CustomerSearchQuery(NamedTuple):
    query: Q
    sorting: Sorting