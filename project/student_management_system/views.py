from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView, View
from django.db.models import Q
from .serializer import StudentUserSerializer, TeacherUserSerializer, UserSerializer, StudentScoreSerializer, CourseSerializer
from .models import StudentUser, TeacherUser, User, Course, StudentScore

from rest_framework_simplejwt.tokens import RefreshToken
import json
from utils.response import result, success, error
from utils.authentication import MyJWTAuthentication
from utils.permissions import IsAuthenticated
from utils.crypto import PrpCrypt
from utils.page import CommonPageNumberPagination as PageNumberPagination
from django_redis import get_redis_connection
from captcha.image import ImageCaptcha
import random
import string
import base64


class Login(View):
    # 登录函数
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        redis_conn = get_redis_connection('verify_code')  # 获取redis连接对象

        # 判断验证码是否传过来了
        if 'uuid' in data:
            uuid = data['uuid']
        else:
            return error('请重新获取验证码')

        # 验证码校验
        captcha = redis_conn.get('img_%s' % data['uuid'])
        if captcha:
            if captcha.decode('utf-8').lower() != data['captcha'].lower():
                return error('验证码错误')
        else:
            return error('验证码已过期')

        # 解密用户名
        prpCrypt = PrpCrypt()
        account = prpCrypt.decrypt(data['account'])

        password = data['password']

        userType = int(data['userType'])
        user_name = ''

        # 用户类型 0学生 1教师 2管理员
        if userType == 0:
            user = StudentUser.objects.filter(account=account).first()
            user_name = user.student_id
        elif userType == 1:
            user = TeacherUser.objects.filter(account=account).first()
            user_name = user.user_name
        elif userType == 2:
            user = User.objects.filter(account=account).first()
            user_name = user.user_name
        else:
            return error("用户类型不存在")

        if user is None:
            return error("用户不存在")
        # 判断用户密码是否正确
        if user.password == password:
            # 手动签发jwt token
            token = RefreshToken.for_user(user)
            resp_data = {
                'user_id': user.id,
                'user_name': user_name,
                'user_type': user.user_type,
                "token": str(token)
            }
            return success(resp_data)
        else:
            return error("密码错误")

# 获取用户权限函数
class UserInfo(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        userType = int(data['userType'])

        user_id = request.user

        data = {
            "roles": "",
            "name": "",
            "avatar": "",
            "introduction": "",
        }

        if userType == 2:
            user = User.objects.filter(id=user_id).first()
            data['roles'] = 'admin'
            data['name'] = user.user_name
        elif userType == 1:
            user = TeacherUser.objects.filter(id=user_id).first()
            data['roles'] = 'teacher'
            data['name'] = user.user_name
        elif userType == 0:
            user = StudentUser.objects.filter(id=user_id).first()
            data['roles'] = 'student'
            data['name'] = user.student_id
        else:
            return error("非法用户禁止登录")

        if user is None:
            return error('用户不存在')



        return success(data)

# 退出登录函数
class Logout(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return result(0, "退出登录成功")

# 获取学生列表函数
class StudentList(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证

    def get(self, request, *args, **kwargs):
        user_id = request.user
        userType = int(request.GET['userType'])
        if userType == 1:
            operateUser = TeacherUser.objects.get(id=user_id)
        elif userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")
        if operateUser is None:
            return error("没有权限")

        paginator = PageNumberPagination()
        paginator.page_size = request.GET['limit']
        sort = request.GET['sort']
        try:
            keywords = request.GET['keywords']
            user = StudentUser.objects.filter(
                Q(account__contains=keywords) | Q(user_name__contains=keywords)).order_by(sort)
        except KeyError as e:
            user = StudentUser.objects.order_by(sort)
        # 分页
        # paginator=PageNumberPagination()
        # 分页过后的数据
        qs = paginator.paginate_queryset(user, request, self)
        # 序列化
        ser = StudentUserSerializer(qs, many=True)

        resData = {
            'count': user.count(),
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': ser.data
        }
        return success(resData)

# 获取学生成绩函数
class StudentScoreList(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证

    def get(self, request, *args, **kwargs):
        uid = request.GET['uid']

        sort = request.GET['sort']
        try:
            keywords = request.GET['keywords']
            studentScore = StudentScore.objects.filter(student=uid).filter(Q(course_name__contains=keywords)).order_by(sort)
        except KeyError as e:
            studentScore = StudentScore.objects.filter(student=uid).order_by(sort)

        return success(list(studentScore.values()))

# 获取学生信息函数
class StudentInfo(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = StudentUserSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user
        student = StudentUser.objects.get(id=user_id)

        rdata = self.serializer_class(student).data
        return success(rdata)

# 获取课程列表函数
class CourseList(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证

    def get(self, request, *args, **kwargs):
        course = Course.objects.filter()

        return success(list(course.values()))

# 获取教师列表函数
class TeacherList(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证

    def get(self, request, *args, **kwargs):
        user_id = request.user
        userType = int(request.GET['userType'])
        if userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")
        if operateUser is None:
            return error("没有权限")

        paginator = PageNumberPagination()
        paginator.page_size = request.GET['limit']
        sort = request.GET['sort']
        try:
            keywords = request.GET['keywords']
            user = TeacherUser.objects.filter(
                Q(account__contains=keywords) | Q(user_name__contains=keywords)).order_by(sort)
        except KeyError as e:
            user = TeacherUser.objects.order_by(sort)
        # 分页
        # paginator=PageNumberPagination()
        # 分页过后的数据
        qs = paginator.paginate_queryset(user, request, self)
        # 序列化
        ser = TeacherUserSerializer(qs, many=True)

        resData = {
            'count': user.count(),
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': ser.data
        }
        return success(resData)

# 注册学生账号函数
class RegisterStudentIndex(View):
    serializer_class = StudentUserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        redis_conn = get_redis_connection('verify_code')  # 获取redis连接对象

        # 判断验证码是否传过来了
        if 'uuid' in data:
            uuid = data['uuid']
        else:
            return error('请重新获取验证码')

        # 验证码校验
        captcha = redis_conn.get('img_%s' % data['uuid'])
        if captcha:
            if captcha.decode('utf-8').lower() != data['captcha'].lower():
                return error('验证码错误')
        else:
            return error('验证码已过期')

        userCount = StudentUser.objects.filter(account=data['account']).count()

        if userCount > 0:
            return error("账户名称已存在")

        user = StudentUser()

        user.account = data['account']
        user.password = data['password']
        user.student_id = data['student_id']
        user.user_type = 0

        if 'gender' in data:
            user.gender = data['gender']
        user.save()
        rdata = self.serializer_class(user).data
        return success(rdata)

# 设置安全问题函数
class SecurityIssues(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = StudentUserSerializer

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        user = StudentUser.objects.get(id=user_id)

        if userType != 0:
            return error("没有权限")

        user.security_issues = data['security_issues']
        user.security_answer = data['security_answer']

        user.save()
        rdata = self.serializer_class(user).data
        return success(rdata)

# 修改学生信息函数
class StudentIndex(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = StudentUserSerializer
    prpCrypt = PrpCrypt()

    # 修改学生信息
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        user = StudentUser.objects.get(id=user_id)

        if userType != 0:
            return error("没有权限")

        user.student_id = data['student_id']

        if 'phone' in data:
            user.phone = data['phone']
        if 'email' in data:
            user.email = data['email']
        if 'address' in data:
            user.address = data['address']
        if 'emergency_contact' in data:
            user.emergency_contact = data['emergency_contact']
        if 'emergency_phone' in data:
            user.emergency_phone = data['emergency_phone']
        if 'major' in data:
            user.major = data['major']

        user.save()
        rdata = self.serializer_class(user).data
        return success(rdata)

    # 删除学生
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 1:
            operateUser = TeacherUser.objects.get(id=user_id)
        elif userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        user = StudentUser.objects.get(id=data['id'])

        if len(user.account) == 0:
            return error("用户不存在")

        # 删除用户
        user.delete()

        rdata = self.serializer_class(user).data
        return success(rdata)

# 修改学生密码函数
class StudentEditPwd(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = StudentUserSerializer
    prpCrypt = PrpCrypt()

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        user = StudentUser.objects.get(id=user_id)

        if userType != 0:
            return error("没有权限")

        if data['security_answer'] != user.security_answer:
            return error("安全问题答案错误")

        user.password = data['password']

        user.save()
        rdata = self.serializer_class(user).data
        return success(rdata)

# 新增修改教师函数
class TeacherIndex(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = TeacherUserSerializer
    prpCrypt = PrpCrypt()

    # 新增教师函数
    def post(self, request, *args, **kwargs):
        # 判断是否为管理员
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        userCount = TeacherUser.objects.filter(account=data['account']).count()

        if userCount > 0:
            return error("账户名称已存在")

        user = TeacherUser()

        user.account = data['account']
        user.password = data['password']
        user.user_type = 1

        if 'user_name' in data:
            user.user_name = data['user_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'email' in data:
            user.email = data['email']
        if 'college' in data:
            user.college = data['college']
        if 'gender' in data:
            user.gender = data['gender']
        user.save()
        rdata = self.serializer_class(user).data
        return success(rdata)

    # 修改教师函数
    def put(self, request, *args, **kwargs):

        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        user = TeacherUser.objects.get(id=data['id'])

        if len(user.account) == 0:
            return error("用户不存在")

        user.password = self.prpCrypt.encrypt(data['password'])

        if 'user_name' in data:
            user.user_name = data['user_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'email' in data:
            user.email = data['email']
        if 'college' in data:
            user.college = data['college']
        if 'gender' in data:
            user.gender = data['gender']
        user.save()
        rdata = self.serializer_class(user).data
        return success(rdata)

    # 删除教师函数
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        user = TeacherUser.objects.get(id=data['id'])

        if len(user.account) == 0:
            return error("用户不存在")

        # 删除用户
        user.delete()
        rdata = self.serializer_class(user).data
        return success(rdata)

# 新增修改课程函数
class CourseIndex(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = CourseSerializer
    prpCrypt = PrpCrypt()

    # 新增课程函数
    def post(self, request, *args, **kwargs):
        # 判断是否为管理员
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        course = Course()

        course.course_name = data['course_name']
        course.sort = data['sort']
        course.save()
        rdata = self.serializer_class(course).data
        return success(rdata)

    # 修改课程函数
    def put(self, request, *args, **kwargs):

        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        course = Course.objects.get(id=data['id'])

        if course is None:
            return error("课程不存在")

        course.course_name = data['course_name']
        course.sort = data['sort']
        course.save()

        rdata = self.serializer_class(course).data
        return success(rdata)

    # 删除课程
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 2:
            operateUser = User.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        course = Course.objects.get(id=data['id'])

        if course is None:
            return error("用户不存在")

        # 删除用户
        course.delete()
        rdata = self.serializer_class(course).data
        return success(rdata)

# 新增修改学生成绩函数
class StudentScoreIndex(APIView):
    permission_classes = [IsAuthenticated, ]  # 权限验证
    authentication_classes = [MyJWTAuthentication, ]  # 权限验证
    serializer_class = TeacherUserSerializer
    prpCrypt = PrpCrypt()

    # 新增学生成绩函数
    def post(self, request, *args, **kwargs):
        # 判断是否为教师
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 1:
            operateUser = TeacherUser.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        studentScore = StudentScore()

        student = StudentUser.objects.get(id=data['student_id'])
        teacher = TeacherUser.objects.get(id=user_id)
        course = Course.objects.get(id=data['course_id'])
        studentScore.course_name = course.course_name
        studentScore.student = student
        studentScore.teacher = teacher
        studentScore.course = course

        if 'grade' in data:
            studentScore.grade = data['grade']
        if 'midterm_exam_score' in data:
            studentScore.midterm_exam_score = data['midterm_exam_score']
        if 'final_exam_score' in data:
            studentScore.final_exam_score = data['final_exam_score']
        studentScore.save()
        return success(1)

    # 修改学生成绩函数
    def put(self, request, *args, **kwargs):

        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 1:
            operateUser = TeacherUser.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        studentScore = StudentScore.objects.get(id=data['id'])

        if studentScore is None:
            return error("成绩不存在")


        course = Course.objects.get(id=data['course_id'])
        studentScore.course_name = course.course_name
        studentScore.course = course

        if 'grade' in data:
            studentScore.grade = data['grade']
        if 'midterm_exam_score' in data:
            studentScore.midterm_exam_score = data['midterm_exam_score']
        if 'final_exam_score' in data:
            studentScore.final_exam_score = data['final_exam_score']
        studentScore.save()
        return success(1)

    # 删除学生成绩函数
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = request.user
        userType = int(data['userType'])
        if userType == 1:
            operateUser = TeacherUser.objects.get(id=user_id)
        else:
            return error("没有权限")

        if operateUser is None:
            return error("没有权限")

        studentScore = StudentScore.objects.get(id=data['id'])

        if studentScore is None:
            return error("成绩不存在")

        # 删除用户
        studentScore.delete()
        return success(1)

# 验证码图片函数
class ImageCodeView(View):

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        img_code = "".join(random.sample(string.ascii_letters + string.digits, 5))

        redis_conn = get_redis_connection('verify_code')  # 获取redis连接对象
        redis_conn.setex('img_%s' % uuid, 120, img_code)
        cap = ImageCaptcha()
        img = cap.generate(img_code)
        encoded_string = base64.b64encode(img.read()).decode('utf-8')
        return success(encoded_string)
