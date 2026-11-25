from pydantic import ValidationError

from app.factory import create_app


try:
    app = create_app()
except ValidationError as exc:
    messages = []
    for error in exc.errors(include_url=False, include_input=False):
        field = ".".join(map(str, error["loc"]))
        if error["type"] == "missing":
            reason = "缺少必填配置"
        elif error["type"] == "extra_forbidden":
            reason = "未知配置项"
        elif (field, error["type"]) == ("log_level", "value_error"):
            reason = str(error["ctx"]["error"])
        else:
            reason = "配置值无效"
        messages.append(f"{field.upper()}：{reason}")
    raise SystemExit("启动失败，配置校验未通过\n" + "\n".join(messages)) from None
