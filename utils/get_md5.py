# md5加密相关
from hashlib import md5
from functools import partial


def get_md5(data):
    """ 获取md5值
    data: 要加密的字符串
    """
    mixer = md5()
    mixer.update(data.encode('utf8'))
    return mixer.hexdigest()


def get_file_md5(data, block_size=65536):
    """ 获取文件md5值
    """
    # 创建md5对象
    m = md5()
    # 对django中的文件对象进行迭代
    for item in iter(partial(data.read, block_size), b''):
        # 把迭代后的bytes加入到md5对象中
        m.update(item)
    str_md5 = m.hexdigest()
    return str_md5

