# md5加密相关
from hashlib import md5


def get_md5(data):
    """ 获取md5值
    data: 要加密的字符串
    """
    mixer = md5()
    mixer.update(data.encode('utf8'))
    return mixer.hexdigest()


if __name__ == '__main__':
    print(get_md5('123456'))

