from ninja import Schema


class PerformanceSchema(Schema):
    execution_time_s: float
    query_count: int