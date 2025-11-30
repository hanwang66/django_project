import json
import logging

from django.utils.deprecation import MiddlewareMixin
from .models import OperationLog

LOG = logging.getLogger(__name__)


class AuditLogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # 1. 如果是 GET 请求，通常不记录（除非你想记录所有查询，那会产生大量数据）
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            # 确实要删掉，不然日志太多了
            LOG.info('begin to mark')
            return

        # 2. 获取当前用户（如果未登录则为 None）
        user = request.user if request.user.is_authenticated else None

        # 3. 判断动作类型
        action = 'OTHER'
        if request.method == 'POST':
            action = 'CREATE' # 或者是 UPDATE，取决于你的业务逻辑，这里简单按方法分
        elif request.method == 'GET':
            action = 'ACCESS'
        elif request.method in ['PUT', 'PATCH']:
            action = 'UPDATE'
        elif request.method == 'DELETE':
            action = 'DELETE'

        # 4. 获取请求参数 (尝试获取 POST 数据或 JSON 数据)
        params = ""
        try:
            if request.method == 'GET':
                # 获取 URL 查询参数
                params = json.dumps(request.GET.dict(), ensure_ascii=False)
            elif request.content_type == 'application/json':
                params = json.dumps(json.loads(request.body), ensure_ascii=False)
            else:
                params = json.dumps(request.POST.dict(), ensure_ascii=False)
        except Exception:
            params = "无法解析参数"

        # 5. 获取 IP 地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # 6. 保存日志
        # 注意：这里不保存敏感信息（如密码），实际项目中建议做过滤
        if 'password' not in params: 
            OperationLog.objects.create(
                user=user,
                action=action,
                path=request.path,
                method=request.method,
                ip_address=ip,
                params=params[:2000] # 截断防止过长
            )

        return None
