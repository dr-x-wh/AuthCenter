# AuthCenter

AuthCenter 是一个使用 Python 3.12、FastAPI、PostgreSQL 和 Redis 的后端服务骨架。

## 本地启动

```bash
uv sync --locked
cp -n .env.example .env
```

按 `.env.example` 中的说明填写 `.env`。后端运行环境、监听 IP、监听端口和两项连接地址均为必填。数据库与 Redis 地址须包含主机名或 IP。配置缺失或无效时，启动入口会列出对应的变量名并退出。

```bash
uv run --locked python -m app.asgi
```

从仓库根目录启动。启动时同名进程环境变量优先于 `.env`，修改配置后需要重启。配置监听 `127.0.0.1:8000` 时，可在 `http://127.0.0.1:8000/docs` 查看接口文档。

## 接口

| 路径 | 行为 |
| --- | --- |
| `GET /health`、`GET /health/live`、`GET /health/startup` | 应用完成启动并响应请求时返回 `200` |
| `GET /health/ready` | 执行 PostgreSQL `SELECT 1` 和 Redis `PING`，均成功时返回 `200`，依赖不可用或探测超时时返回 `503` |
| `GET /login` | 认证预留入口，返回 `501` |

## 工程结构

```text
app/
├── asgi.py          校验配置并按配置启动 Uvicorn
├── factory.py       创建应用并挂载路由
├── lifespan.py      初始化和释放应用级资源
├── api/             HTTP 路由和请求级依赖
├── core/            配置和日志
├── extensions/      PostgreSQL 会话工厂和 Redis 客户端
└── models/          SQLAlchemy 模型基类
```

`factory.py` 组装路由和应用生命周期。生命周期通过 `extensions` 管理连接资源，路由通过 `api/deps.py` 注入请求级数据库会话与共享 Redis 客户端。数据库会话在请求结束时关闭，写操作由调用方决定何时提交。
