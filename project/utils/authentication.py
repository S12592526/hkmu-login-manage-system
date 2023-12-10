from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken

from student_management_system.models import StudentUser, TeacherUser, User

# 自定义的解析token的方法 下面会用到
from utils.token_get_user import get_user_id


class MyJWTAuthentication(JWTAuthentication):
    """
    继承JWTAuthentication类， 返回自定义User对象
    """

    # get_user用于返回用户，重写后在其它地方使用request.user时可以直接得到自定义的小程序用户
    def get_user(self, validated_token):
        # try:
        #     validated_token = RefreshToken({"token": validated_token})
        #     # 如果令牌有效，则不会引发异常。
        # except Exception as e:
        #     # 如果令牌无效，则会引发异常。
        #     print(e)
        #     return None
        try:
            user_id = get_user_id(validated_token)  # 此处为自定义的解析token方法， 可以解码token得到其中的信息，重点是拿到user_id 用于后续的获取用户
        except KeyError:
            raise InvalidToken(('Token不包含可识别的用户标识'))

        return user_id

    def authenticate(self, request):
        # 自定义身份验证逻辑，例如检查请求头中是否包含特定参数等。
        token = request.META.get("HTTP_TOKEN")
        if token:
            user = self.get_user(token)
            return user, None
        else:
            return super().authenticate(request)
