from django.db import models
from django.utils import timezone


# Create your models here.

class StudentUser(models.Model):
    USERTYPE = ((1, '教师'),
                (2, '管理员'),
                (0, '学生'))

    account = models.CharField('账户', max_length=100, blank=True)
    password = models.CharField('密码', max_length=100, blank=True)
    student_id = models.CharField('学号', max_length=100, blank=True)
    email = models.CharField('用户邮箱', max_length=100, blank=True)
    phone = models.BigIntegerField('手机号', unique=True, blank=True, null=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    emergency_contact = models.CharField('紧急联系人', max_length=255, blank=True, null=True)
    emergency_phone = models.CharField('紧急联系电话', max_length=255, blank=True, null=True)
    security_issues = models.CharField('安全问题', max_length=255, blank=True, null=True)
    security_answer = models.CharField('安全问题答案', max_length=255, blank=True, null=True)
    major = models.CharField('专业', max_length=255, blank=True, null=True)
    user_type = models.IntegerField('用户类型', choices=USERTYPE, default=0)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def __str__(self):
        return self.user_name

    class Meta:
        managed = False
        db_table = 'student_user'
        verbose_name = '学生用户管理'
        verbose_name_plural = verbose_name


class TeacherUser(models.Model):
    GENDER = ((1, '男'),
              (2, '女'),
              (0, '未知'))
    USERTYPE = ((1, '教师'),
                (2, '管理员'),
                (0, '学生'))

    account = models.CharField('账户', max_length=100, blank=True)
    password = models.CharField('密码', max_length=100, blank=True)
    user_name = models.CharField('用户名', max_length=100, blank=True)
    email = models.CharField('用户邮箱', max_length=100, blank=True)
    phone = models.CharField('手机号', max_length=11, blank=True, null=True)
    gender = models.IntegerField('性别', choices=GENDER, default=0)
    college = models.CharField('学院', max_length=255, blank=True, null=True)
    user_type = models.IntegerField('用户类型', choices=USERTYPE, default=0)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def __str__(self):
        return self.user_name

    class Meta:
        managed = False
        db_table = 'teacher_user'
        verbose_name = '教师用户管理'
        verbose_name_plural = verbose_name


class User(models.Model):
    USERTYPE = ((1, '教师'),
                (2, '管理员'),
                (0, '学生'))

    account = models.CharField('账户', max_length=100, blank=True)
    password = models.CharField('密码', max_length=100, blank=True)
    user_name = models.CharField('用户名', max_length=100, blank=True)
    email = models.CharField('用户邮箱', max_length=100, blank=True)
    phone = models.BigIntegerField('手机号', unique=True, blank=True, null=True)
    user_type = models.IntegerField('用户类型', choices=USERTYPE, default=0)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def __str__(self):
        return self.account

    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = '管理员用户管理'
        verbose_name_plural = verbose_name


class Course(models.Model):
    course_name = models.CharField('课程名称', max_length=100, blank=True)
    sort = models.IntegerField('排序', default=0)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def __str__(self):
        return self.course_name

    class Meta:
        db_table = 'course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class StudentScore(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    student = models.ForeignKey(StudentUser, on_delete=models.PROTECT)
    teacher = models.ForeignKey(TeacherUser, on_delete=models.PROTECT)
    course_name = models.CharField('课程名称', max_length=100, blank=True)
    grade = models.CharField('作业分数', max_length=100, blank=True)
    midterm_exam_score = models.CharField('期中考试成绩', max_length=100, blank=True)
    final_exam_score = models.CharField('期末考试成绩', max_length=100, blank=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def __str__(self):
        return self.student

    class Meta:
        db_table = 'student_score'
        verbose_name = '学生成绩'
        verbose_name_plural = verbose_name
