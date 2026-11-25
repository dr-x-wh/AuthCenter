# AuthCenter

AuthCenter 是一个使用 Python 3.12、FastAPI、PostgreSQL 和 Redis 的后端服务骨架。

## 本地启动

```bash
uv sync --locked
cp -n .env.example .env
```

在 `.env` 中填入可用的 PostgreSQL 和 Redis 连接地址，再从仓库根目录启动服务。

```bash
uv run --locked uvicorn app.asgi:app --reload
```

| 环境变量 | 用途 |
| --- | --- |
| `DATABASE_URL` | PostgreSQL 连接地址。支持 `postgresql+asyncpg://`、`postgresql://` 和 `postgres://`，也可使用 `POSTGRES_URL` |
| `REDIS_URL` | Redis 连接地址 |
| `APP_NAME` | 服务名称，默认 `AuthCenter` |
| `APP_DEBUG` | FastAPI 调试模式，默认 `false` |
| `LOG_LEVEL` | 应用日志级别，默认 `INFO` |

启动后可在 `http://127.0.0.1:8000/docs` 查看接口文档。

## 接口

| 路径 | 行为 |
| --- | --- |
| `GET /health`、`GET /health/live`、`GET /health/startup` | 应用完成启动并响应请求时返回 `200` |
| `GET /health/ready` | 执行 PostgreSQL `SELECT 1` 和 Redis `PING`，均成功时返回 `200`，依赖不可用或探测超时时返回 `503` |
| `GET /login` | 认证预留入口，返回 `501` |

## 工程结构

```text
app/
├── asgi.py          Uvicorn 入口
├── factory.py       创建应用并挂载路由
├── lifespan.py      初始化和释放应用级资源
├── api/             HTTP 路由和请求级依赖
├── core/            配置和日志
├── extensions/      PostgreSQL 会话工厂和 Redis 客户端
└── models/          SQLAlchemy 模型基类
```

`factory.py` 组装路由和应用生命周期。生命周期通过 `extensions` 管理连接资源，路由通过 `api/deps.py` 注入请求级数据库会话与共享 Redis 客户端。数据库会话在请求结束时关闭，写操作由调用方决定何时提交。
