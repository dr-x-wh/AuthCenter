# AuthCenter

AuthCenter 是一个使用 Python 3.12、FastAPI、PostgreSQL 和 Redis 的后端服务骨架。

## 本地启动

```bash
uv sync --locked
cp -n .env.example .env
```

按 `.env.example` 中的说明填写 `.env`。后端运行环境、监听 IP、监听端口和两项连接地址均为必填。数据库与 Redis 地址须指定主机名或 IP。缺少必填项时会指出变量名并退出，连接参数由对应客户端处理。

```bash
uv run --locked python -m app.asgi
```

从项目根目录执行时，`app.asgi` 读取 `.env`，按 `UVICORN_HOST` 和 `UVICORN_PORT` 启动 Uvicorn。同名进程环境变量优先于 `.env`，修改配置后需要重启。

`BACKEND_ENV=development` 时开放 `/docs`、`/redoc` 和 `/openapi.json`，并允许使用 `debug` 日志级别。生产环境的 `UVICORN_LOG_LEVEL` 接受 `info`、`warning` 和 `error`。异常堆栈由服务端记录。

也可以让 Uvicorn 按标准导入路径加载同一个模块，由 uv 在启动前载入 `.env`。

```bash
uv run --locked --env-file .env uvicorn app.asgi:app
```

## 接口

| 路径 | 行为 |
| --- | --- |
| `GET /health`、`GET /health/live`、`GET /health/startup` | 应用完成启动并响应请求时返回 `200` |
| `GET /health/ready` | 执行 PostgreSQL `SELECT 1` 和 Redis `PING`，均成功时返回 `200`，依赖不可用或探测超时时返回 `503` |
| `GET /login` | 认证预留入口，返回 `501` |

API 的成功和错误响应使用统一的 `Result` 结构，包含 `data`、`code` 和 `message`。成功时 `code` 为 `0`，错误时与 HTTP 状态码一致。全局处理器负责封装 HTTP 异常、请求校验失败和未处理异常。接口路径按声明匹配，多余的尾斜杠会触发 `404`。

开发环境的文档页面和 OpenAPI 描述保留各自的标准格式。

## 工程结构

```text
app/
├── asgi.py          导出 ASGI 应用
├── factory.py       创建应用并挂载路由
├── lifespan.py      初始化和释放应用级资源
├── api/             HTTP 路由和请求级依赖
├── core/            配置和日志
├── extensions/      PostgreSQL 会话工厂和 Redis 客户端
└── models/          SQLAlchemy 模型基类
```

`api/routes/__init__.py` 汇总并导出 `routers` 列表，`api/router.py` 按列表顺序注册路由。`factory.py` 挂载总路由并配置应用生命周期。路由较多时，可由各业务子包汇总自己的列表，再由父包合并。

生命周期通过 `extensions` 管理连接资源，路由通过 `api/deps.py` 注入请求级数据库会话与共享 Redis 客户端。数据库会话在请求结束时关闭，写操作由调用方决定何时提交。
