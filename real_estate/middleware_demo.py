import logging
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from functools import wraps

# 获取日志记录器
logger = logging.getLogger(__name__)

# 定义错误原因常量 (模仿 csrf.py 的风格)
REASON_NO_KEY = "API Key missing."
REASON_BAD_KEY = "API Key incorrect."

class ApiKeyMiddleware(MiddlewareMixin):
    """
    一个自定义中间件，用于检查请求头中是否包含正确的 X-API-KEY。
    参照 CsrfViewMiddleware 的结构实现。
    """

    def _reject(self, request, reason):
        """
        拒绝请求的辅助方法 (模仿 csrf.py 的 _reject)
        """
        logger.warning(f"Forbidden ({reason}): {request.path}")
        response = JsonResponse({"error": "Forbidden", "reason": reason}, status=403)
        return response

    def _get_api_key(self, request):
        """
        从请求头获取 API Key (模仿 csrf.py 的 _get_secret)
        """
        return request.META.get("HTTP_X_API_KEY")

    def process_request(self, request):
        print("API Key Middleware: process_request called", flush=True)
        print(request.COOKIES)
        print(settings.CSRF_COOKIE_NAME)
        """
        请求进入时的预处理 (模仿 csrf.py 的 process_request)
        """
        # 这里可以做一些初始化工作，或者记录日志
        logger.info(f"ApiKeyMiddleware: Processing request {request.path}")
        return None  # 返回 None 表示继续执行下一个中间件

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        视图函数执行前的校验逻辑 (模仿 csrf.py 的 process_view)
        """
        # 1. 检查视图是否被标记为豁免 (类似 csrf_exempt)
        if getattr(callback, "api_key_exempt", False):
            logger.info("View is exempt from API Key check.")
            return None

        # 2. 假设我们只拦截 /api/ 开头的路径
        if not request.path.startswith("/api/"):
            return None

        # 3. 获取并校验 Key
        api_key = self._get_api_key(request)
        
        if not api_key:
            return self._reject(request, REASON_NO_KEY)

        # 获取 settings 中的配置密钥，如果没有配置则使用默认值
        expected_key = getattr(settings, "MY_SECRET_API_KEY", "123456")

        # 简单的字符串比较 (生产环境建议使用 constant_time_compare 防止时序攻击)
        if api_key != expected_key:
            return self._reject(request, REASON_BAD_KEY)

        return None  # 校验通过

    def process_response(self, request, response):
        """
        响应返回前的处理 (模仿 csrf.py 的 process_response)
        """
        # 可以在这里添加自定义响应头
        response["X-API-Key-Checked"] = "True"
        return response

# --- 配套的装饰器 ---

def api_key_exempt(view_func):
    """
    将视图标记为豁免 API Key 检查 (模仿 csrf_exempt)
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    
    wrapped_view.api_key_exempt = True
    return wraps(view_func)(wrapped_view)
