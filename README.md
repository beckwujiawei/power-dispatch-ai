# 电力通信调度智能助手

这是一个用于开发和演示的 FastAPI 调度助手。当前默认使用模拟模型，不连接生产系统；后续部署到电力内网后，可以通过环境变量切换到光明大模型适配模式。

## 本地运行

```powershell
cd C:\wu\power-dispatch-ai
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

浏览器打开：

```text
http://127.0.0.1:8000/
```

## 配置模型模式

复制 `.env.example` 的内容到项目根目录的 `.env`，或者在启动前设置环境变量。当前代码默认：

```text
MODEL_PROVIDER=mock
```

配置状态可通过以下地址查看（不会返回 API 密钥）：

```text
http://127.0.0.1:8000/api/config/model
```

支持的提供方标识：

- `mock`：本地模拟模式，适合当前开发
- `deepseek`：预留给允许访问公网 API 的测试环境
- `guangming`：预留给电力内网部署

目前 `deepseek` 和 `guangming` 仅完成配置层预留，实际请求适配应在确认网络、鉴权和数据安全要求后实现。

## 主要接口

- `GET /api/health`：服务和模型配置状态
- `GET /api/alerts`：模拟通信告警
- `POST /api/dispatch/chat`：调度对话
- `POST /api/audit/confirm`：保存人工确认
- `GET /api/audit/logs`：读取审计记录
