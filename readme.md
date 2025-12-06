
# Django 综合信息管理平台

本项目为基于 Django 5.x 的多模块信息管理系统，支持博客、房地产、股票行情等功能，界面美观，支持多用户管理。

## 项目启动步骤

1. 克隆或下载本项目到本地。

2. 进入项目目录，建议使用 Python 虚拟环境：
   ```powershell
   # Python 3.10.0
   python -m venv .venv
   .\venv\Scripts\Activate.ps1
   git push -u origin feature/blog main
   ```

3. 安装依赖包：
   ```powershell
   pip install -r requirements.txt
   pip freeze > requirements.txt 
   ```

4. 数据库迁移：
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

5. 创建超级用户（如需后台管理）：
   ```powershell
   python manage.py createsuperuser
   ```

6. 启动项目：
   ```powershell
   python manage.py runserver
   ```

7. 在浏览器访问 http://127.0.0.1:8000/

8. 默认管理员账号：admin / admin

## 主要功能模块

- 首页：Tab 布局，快速跳转各模块页面
- 博客模块：博客增删改查、详情、评论、点赞（/blog/）
- 房地产模块：信息录入、列表、详情、编辑、删除（/real_estate/）
- 股票行情模块：行情展示与自定义股票观察（/stock/）
- 用户与安全：支持 Django 后台管理，权限可扩展

## 日志与异常监控
- 所有操作和异常会记录到 `app.log` 文件
- 未捕获异常显示友好错误页面

## 前端界面
- 现代风格，首页为 Tab 布局，所有功能分区清晰
- 支持移动端适配（可进一步优化）

## 依赖说明
- 详见 requirements.txt，核心依赖：Django、pandas、openpyxl、reportlab 等

## 扩展建议
- 权限控制、密码加密、API接口、富文本编辑、评论管理、分页筛选、第三方登录等

如需英文文档或更多接口示例，请补充需求！