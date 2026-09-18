# 电力通信调度智能助手：内网容器部署

## 1. 部署前准备

在部署主机安装 Docker Engine 和 Docker Compose Plugin，并将项目复制到内网主机。不要把真实密钥提交到 Git。

创建部署配置：

```bash
cp .env.example .env
```

默认使用本地模拟模型，适合先验证容器和网页：

```dotenv
MODEL_PROVIDER=mock
MODEL_NAME=mock-dispatch-model
MODEL_BASE_URL=
MODEL_TIMEOUT=30
APP_PORT=8000
```

如果接入内网模型网关，再由部署管理员填写实际的 `MODEL_PROVIDER`、`MODEL_NAME` 和 `MODEL_BASE_URL`；当前模型适配层仍是配置预留，接入前需要按网关协议实现请求适配、鉴权和安全审查。

## 2. 构建与启动

```bash
docker compose build --no-cache
docker compose up -d
```

查看状态和日志：

```bash
docker compose ps
docker compose logs -f power-dispatch-ai
```

访问：

```text
http://<内网主机地址>:8000/
```

健康检查：

```text
http://<内网主机地址>:8000/api/health
```

## 3. 数据持久化

`docker-compose.yml` 使用 Docker named volume `power_dispatch_data` 保存运行时数据。容器重建不会丢失：

- `audit_logs.json`
- `tickets.json`

查看卷：

```bash
docker volume inspect power-dispatch-ai_power_dispatch_data
```

当前应用代码默认从项目根目录读取 JSON 文件；因此生产内网部署前，应将数据目录通过环境变量或统一存储路径接入应用。若暂时保持现状，请确认容器内 `/app` 可写，并在升级前备份数据文件。

## 4. 停止与升级

```bash
docker compose down
git pull origin main
docker compose build --no-cache
docker compose up -d
```

仅停止容器但保留数据卷：

```bash
docker compose down
```

不要执行 `docker compose down -v`，除非确认可以删除本地工单和审计数据。

## 5. 内网安全建议

- 不要直接将 8000 端口暴露到办公网，建议由内网反向代理统一提供 HTTPS、访问控制和审计。
- 通过防火墙限制来源网段，只允许调度工作站访问。
- 将 `.env` 放在部署主机并限制文件权限，不纳入版本库。
- 生产环境建议把 JSON 文件替换为 PostgreSQL/MySQL 等受控数据库，并配置备份、并发写入和权限管理。
- 接入真实告警、模型网关和工单系统前，先完成网络分区、数据分级、鉴权、日志留存和安全评审。
- 继续保留人工确认，不要让模型直接执行生产控制操作。
