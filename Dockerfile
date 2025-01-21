# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9-slim AS builder

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件
COPY requirements.txt /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 使用多阶段构建
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 从 builder 阶段复制已安装的依赖
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# 复制应用程序代码
COPY . /app

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["python", "app.py"]
