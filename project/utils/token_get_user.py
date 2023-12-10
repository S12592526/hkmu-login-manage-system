import jwt
import time

# 此处导入的是项目的settings，主要是拿到自定义的secret_key
from project import settings
from datetime import timedelta


def get_user_id(t):
    """根据token得到当前用户user_id"""
    try:
        decode_data = jwt.decode(t, secret_key=settings.SECRET_KEY, verify=False, algorithms=['HS256'])
        if int(decode_data['exp']) < int(time.time()):
            print("token过期")
            return False
        return decode_data['user_id']
    except Exception as e:
        print("token错误:\n" + str(e))
        return False
