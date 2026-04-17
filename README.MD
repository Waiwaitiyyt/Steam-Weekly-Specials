# Steam Weekly Specials

自动获取 Steam 当前打折游戏信息，生成 HTML 邮件并定期发送到指定邮箱。

---

## 功能

- 从 Steam 商店 API 获取当前特惠游戏列表
- 提取游戏名称、原价、折后价、折扣力度及封面图
- 使用 Jinja2 渲染为 HTML 邮件
- 通过 SMTP 发送到指定邮箱
- 支持部署到树莓派，配合 cron 定时运行

---

## 项目结构

```
steam_specials/
├── main.py          # 主入口
├── fetch.py         # Steam API 数据获取
├── render.py        # Jinja2 HTML 渲染
├── send.py          # SMTP 邮件发送
├── template.html    # 邮件 HTML 模板
├── config.json      # 配置文件（见下方说明）
├── setup.sh         # 一键部署脚本
└── README.md
```

---

## 安装与配置

### 1. 克隆仓库

```bash
git clone https://github.com/Waiwaitiyyt/Steam-Weekly-Specials.git steam_deals
cd steam_deals
```

### 2. 安装依赖

```bash
pip3 install requests jinja2 python-dotenv --break-system-packages
```

### 3. 配置 `config.json`

```json
{
    "url": "https://store.steampowered.com/search/results/",
    "detail_url": "https://store.steampowered.com/api/appdetails/",
    "params": {
        "specials": 1,
        "count": 25,
        "cc": "CN",
        "json": 1
    },
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "sender_email": "you@example.com",
    "recipients_list": ["recipient@example.com"],
    "password": "your_password"
}
```
smpt的密码要预先获取。

`cc` 字段为地区代码，影响价格货币单位及游戏可用性，例如 `CN`、`AU`、`US`。

### 4. SMTP 端口说明

| 端口 | 说明 |
|------|------|
| 587  | STARTTLS，`use_tls: true`（默认） |
| 465  | SSL 直连，需修改 `send.py` 使用 `SMTP_SSL` |

---

## 运行

```bash
python3 main.py
```

---

## 树莓派自动部署

运行一键部署脚本，自动安装依赖、创建运行脚本并添加 cron job：

```bash
chmod +x setup.sh
./setup.sh
```

默认设置为**每周一早上 8 点**自动运行，运行日志保存至 `log.txt`。

如需修改运行时间，编辑 cron：

```bash
crontab -e
```

cron 时间格式参考：

```
# 分 时 日 月 周
  0  8  *  *  1   # 每周一 08:00
  0  9  *  *  5   # 每周五 09:00
```

---

## 注意事项

- Steam 商店 API 为非官方接口，Valve 未提供正式文档，接口结构可能随时变化
- 部分游戏因区域限制可能返回失败，程序会自动跳过
- 请求间隔默认 1 秒，避免触发 IP 限制