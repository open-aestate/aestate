# -*- utf-8 -*-
# 请求响应等
class Request:
    pass


class Response:
    pass


class HttpRequest(Request):
    pass


class HttpResponse(Response):
    pass


class ResponseBody(HttpResponse):
    pass


class GetMapping(HttpRequest):
    pass


class PostMapping(HttpRequest):
    pass


class PutMapping(HttpRequest):
    pass


class DeleteMapping(HttpRequest):
    pass


# 字段属性等
class Param:
    pass


class RequestParam(Param):
    pass


class CookiesParam(Param):
    pass


class SessionParam(Param):
    pass
