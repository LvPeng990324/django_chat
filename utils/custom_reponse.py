from django.http import JsonResponse


def base_response(code, message, data):
    """ 基础响应
    以下的自定义响应调用这个
    """
    response_data = {
        'code': code,
        'message': message,
        'data': data,
    }
    return JsonResponse(data=response_data)


def response_200(message, data):
    """ 自定义200响应
    """
    return base_response(code=200, message=message, data=data)


def response_404(message, data=None):
    """ 自定义404响应
    """
    if data is None:
        data = {}
    return base_response(code=404, message=message, data=data)


def response_403(message, data=None):
    """ 自定义403响应
    """
    if data is None:
        data = {}
    return base_response(code=404, message=message, data=data)


def response_400(message, data=None):
    """ 自定义400响应
    """
    if data is None:
        data = {}
    return base_response(code=404, message=message, data=data)



