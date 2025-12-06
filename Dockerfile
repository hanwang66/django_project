FROM python:3.11

WORKDIR /app

# 覆盖 apt 源为阿里云（适用于 bookworm/trixie）
RUN echo "deb http://mirrors.aliyun.com/debian trixie main contrib non-free non-free-firmware\n\
deb http://mirrors.aliyun.com/debian trixie-updates main contrib non-free non-free-firmware\n\
deb http://mirrors.aliyun.com/debian-security trixie-security main contrib non-free non-free-firmware" \
> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]