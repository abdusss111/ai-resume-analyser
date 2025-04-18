import time
import logging
from django.db import connection

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        sql_queries = len(connection.queries)
        
        logger.info(f"""
            Path: {request.path}
            Method: {request.method}
            Duration: {duration:.2f}s
            Queries: {sql_queries}
            Status: {response.status_code}
        """)

        return response 