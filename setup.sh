#!/bin/bash

USER_NAME=$(whoami)
PROJECT_DIR="/home/$USER_NAME/steam_deals"
PYTHON="/usr/bin/python3"

echo ">>> 检测到用户: $USER_NAME"
echo ">>> 项目目录: $PROJECT_DIR"

echo ">>> 安装依赖..."
pip3 install requests jinja2 python-dotenv --break-system-packages

echo ">>> 创建运行脚本..."
cat > "$PROJECT_DIR/run.sh" << EOF
#!/bin/bash
cd $PROJECT_DIR
/usr/bin/python3 main.py >> $PROJECT_DIR/log.txt 2>&1
EOF
chmod +x "$PROJECT_DIR/run.sh"

echo ">>> 添加 cron job..."
CRON_JOB="0 8 * * 1 $PROJECT_DIR/run.sh"
( crontab -l 2>/dev/null | grep -v "steam_deals"; echo "$CRON_JOB" ) | crontab -

echo ">>> 验证 cron..."
crontab -l

echo ">>> 完成。每周一早8点自动运行"