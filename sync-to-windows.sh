#!/bin/bash
# 同步脚本：将构建结果同步到 Windows 目录

LINUX_DIR="/home/mako/wiki"
WINDOWS_DIR="/mnt/c/Users/ROG/.openclaw/workspace/projects/daily-intel/gwern.net"

echo "=== Gwern.net 构建同步脚本 ==="

# 激活 Haskell 环境
source ~/.ghcup/env

# 在 Linux 目录下构建
echo ">>> 开始构建..."
cd "$LINUX_DIR/build"
cabal run hakyll -- build

if [ $? -eq 0 ]; then
    echo ">>> 构建成功！同步到 Windows..."

    # 同步生成的网站
    rsync -av --delete "$LINUX_DIR/_site/" "$WINDOWS_DIR/_site/"

    # 同步源文件（可选）
    rsync -av "$LINUX_DIR/blog/" "$WINDOWS_DIR/blog/"
    rsync -av "$LINUX_DIR/metadata/" "$WINDOWS_DIR/metadata/"

    echo ">>> 同步完成！"
    echo ">>> Windows 路径: $WINDOWS_DIR/_site/"
else
    echo ">>> 构建失败！"
    exit 1
fi
