import os
import sys
import django

# 1. 设置项目根目录
# 获取当前脚本所在目录的上一级目录 (即项目根目录 django_project)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 2. 设置 Django 环境变量
# 确保 'iproject.settings' 是你 settings.py 的正确路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iproject.settings")

# 3. 初始化 Django
django.setup()

# 4. 导入模型 (必须在 django.setup() 之后)
from tickets.models import OperationLog
from django.db.models import Q

def delete_invalid_logs():
    print("开始清理无效日志...")

    # --- 定义什么是“无效日志” ---
    # 例如：
    # 1. 删除所有静态文件的访问记录 (以 /static/ 开头)
    # 2. 删除所有后台 Admin 的自动请求 (以 /admin/jsi18n/ 开头)
    # 3. 删除 favicon.ico 的请求
    # 4. 删除没有用户的 GET 请求 (匿名访问)
    
    invalid_logs = OperationLog.objects.filter(
        method='GET'
    )

    count = invalid_logs.count()
    
    if count > 0:
        # 执行删除
        # invalid_logs.delete() # 真正删除时取消注释这一行
        print(f"找到 {count} 条无效日志。")
        print("示例日志:")
        for log in invalid_logs[:5]:
            print(f" - [{log.method}] {log.path}")

        deleted_count, _ = invalid_logs.delete()
        print(f"成功删除 {deleted_count} 条日志。")
    else:
        print("没有发现无效日志。")

if __name__ == "__main__":
    delete_invalid_logs()