from rest_framework import serializers
from .models import StudentUser, TeacherUser, User, StudentScore, Course


class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUser
        fields = ("id", "student_id", "account", "password", "phone", "email", "address",
                  "emergency_contact", "emergency_phone", "security_issues", "security_answer", "major")


class TeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherUser
        fields = ("id", "user_name", "account", "password", "phone", "email", "gender", "college")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "user_name", "account", "password", "phone", "email")


class StudentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScore
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
