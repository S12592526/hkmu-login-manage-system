
# urls.py
from django.urls import path
from student_management_system.views import Login, UserInfo, Logout, RegisterStudentIndex, StudentEditPwd, SecurityIssues, StudentInfo, StudentScoreIndex, CourseIndex, StudentIndex, TeacherIndex, StudentList, CourseList, StudentScoreList, TeacherList, ImageCodeView

# 后台路由配置
urlpatterns = [
    path('login', Login.as_view()),
    path('userInfo', UserInfo.as_view()),
    path('logout', Logout.as_view()),
    path('registerStudent', RegisterStudentIndex.as_view()),
    path('student', StudentIndex.as_view()),
    path('studentEditPwd', StudentEditPwd.as_view()),
    path('teacher', TeacherIndex.as_view()),
    path('studentScore', StudentScoreIndex.as_view()),
    path('course', CourseIndex.as_view()),
    path('courseList', CourseList.as_view()),
    path('studentList', StudentList.as_view()),
    path('studentInfo', StudentInfo.as_view()),
    path('setSecurityIssues', SecurityIssues.as_view()),
    path('studentScoreList', StudentScoreList.as_view()),
    path('teacherList', TeacherList.as_view()),
    path('captcha/<str:uuid>/', ImageCodeView.as_view()),
]
