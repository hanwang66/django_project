import logging
import time

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 请求阶段：记录请求信息
        logger.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        # 响应阶段：记录响应信息
        logger.info(f"Response: {response.status_code}")
        return response


class PerformanceMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 请求开始时间
        start_time = time.time()

        # 处理请求
        response = self.get_response(request)

        # 请求结束时间
        end_time = time.time()
        duration = end_time - start_time

        # 记录性能日志
        logger.info(
            f"Performance: {request.method} {request.path} took {duration:.2f} seconds"
        )

        return response