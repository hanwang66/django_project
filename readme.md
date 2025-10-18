# 综合信息管理系统
## 项目启动步骤

1. 克隆或下载本项目到本地。

2. 进入项目目录，建议使用 Python 虚拟环境：
  ```powershell
  python -m venv .venv

  # 激活服务
 .venv\\Scripts\\activate.bat
  # 启动服务
python manage.py runserver
  ```

3. 安装所有依赖包：
  ```powershell
  pip install -r requirements.txt
  ```

4. 启动项目：
  ```powershell
  python app.py
  ```

5. 首次启动会自动初始化数据库（data.db），如需重置可删除该文件。

6. 在浏览器访问 http://127.0.0.1:5000

7. 默认管理员账号：admin / admin

8. Swagger API文档自动生成，访问地址：
  - http://127.0.0.1:5000/apidocs
  - 可在线查看所有接口、参数和操作方法

### 信息录入模块

### 英语学习模块

### 房地产信息模块
  - 搜索参数：query（小区名或城市，POST方式）

### 用户与安全


### 博客模块
## 股票行情模块

  - 用户可在股票行情页面输入股票代码和市场类型（沪/深），点击“添加观察”后自动保存。
  - 所有已添加的自定义股票会在行情页面下方自动展示，实时显示最新价格。
  - 支持多只股票同时观察。
  - `POST /blog/<id>/comment`：发表评论（需登录）
  - `POST /blog/<id>/like`：点赞（需登录）
  - `POST /blog/<id>/unlike`：取消点赞（需登录）

## 日志与异常监控

## 前端界面

## 扩展建议

如需英文文档或更多接口示例，请补充需求！

# Django 综合信息管理平台

本项目为基于 Django 5.x 的多模块信息管理系统，支持博客、信息录入、股票行情、房地产等功能，界面美观，支持多用户管理。

## 项目启动步骤

1. 克隆或下载本项目到本地。

2. 进入项目目录，建议使用 Python 虚拟环境：
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

3. 安装依赖包：
  ```powershell
  pip install -r requirements.txt
  ```

4. 数据库迁移：
  ```powershell
  python manage.py makemigrations
  python manage.py migrate
  ```

5. 创建超级用户（默认 admin/admin，已自动创建）：
  ```powershell
  python manage.py createsuperuser
  ```

6. 启动项目：
  ```powershell
  python manage.py runserver
  ```

7. 在浏览器访问 http://127.0.0.1:8000/

8. 默认管理员账号：admin / admin

## 功能模块

### 首页
- 竖排 Tab 布局，点击可跳转各模块页面。

### 博客模块
- 博客增删改查、详情、评论、点赞
- 路径：/blog/

### 信息录入模块
- 信息增删改查、详情
- 路径：/info/

### 房地产模块
- 房地产信息录入、列表、详情、编辑、删除
- 路径：/real_estate/

### 股票行情模块
- 股票行情展示与自定义股票观察
- 路径：/stock/

### 用户与安全
- 支持 Django 后台管理，权限可扩展

## 日志与异常监控
- 所有操作和异常会记录到 `app.log` 文件
- 未捕获异常显示友好错误页面

## 前端界面
- 现代风格，首页为 Tab 布局，所有功能分区清晰
- 支持移动端适配（可进一步优化）

## 扩展建议
- 权限控制、密码加密、API接口、富文本编辑、评论管理、分页筛选、第三方登录等

如需英文文档或更多接口示例，请补充需求！