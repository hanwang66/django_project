#!/bin/bash

# docker-to-ctr.sh
# 将本地所有 Docker 镜像导出为 tar 并存储到指定目录
# 若目标 tar 已存在则跳过

DIR="/home/hanwang/docker_images"

set -e

# 创建存储目录
mkdir -p "$DIR"

echo "🔍 获取本地 Docker 镜像列表..."
IMAGES=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>")

if [ -z "$IMAGES" ]; then
  echo "❌ 未找到有效的 Docker 镜像（排除 <none> 标签）"
  exit 1
fi

COUNT=$(echo "$IMAGES" | wc -l)
echo "📦 共找到 ${COUNT} 个镜像，开始保存到 ${DIR} ..."

for img in $IMAGES; do
  echo "➡️  处理镜像: $img"
  
  # 目标 tar 文件名：将仓库/标签中的特殊字符替换为下划线
  TARGET_TAR="${DIR}/$(echo "$img" | tr '/' '_' | tr ':' '_').tar"

  if [ -f "$TARGET_TAR" ]; then
    echo "⏭️  已存在：$TARGET_TAR，跳过保存"
    continue
  fi

  echo "💾 保存镜像为 tar：$TARGET_TAR"
  docker save "$img" -o "$TARGET_TAR"
  # 导入到 containerd 的 k8s.io 命名空间（Kubernetes 使用此命名空间）
  ctr -n k8s.io images import --no-unpack "$TARGET_TAR"
  
  echo "✅ 镜像 $img 已导入 containerd"
  echo "✅ 已保存：$TARGET_TAR"
done

echo "🎉 所有镜像保存完成！"
echo "📂 存储目录：$DIR"
