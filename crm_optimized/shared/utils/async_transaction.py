from concurrent.futures import ThreadPoolExecutor
from django.db.transaction import Atomic
from asgiref.sync import sync_to_async
from django.db import connections
from asyncio import wrap_future


class AsyncAtomicContextManager(Atomic):

    def __init__(self, using=None, savepoint=True, durable=False):
        super().__init__(using, savepoint, durable)
        self.executor = ThreadPoolExecutor(1)

    async def __aenter__(self):
        await sync_to_async(super().__enter__, thread_sensitive=False, executor=self.executor)()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await sync_to_async(super().__exit__, thread_sensitive=False, executor=self.executor)(exc_type, exc_value,
                                                                                              traceback)
        future = wrap_future(self.executor.submit(self.close_connections))
        await future
        self.executor.shutdown()

    async def run_in_context(self, fun, *args, **kwargs):
        future = wrap_future(self.executor.submit(fun, *args, **kwargs))
        await future
        return future.result()

    def close_connections(self):
        for conn in connections.all():
            conn.close()