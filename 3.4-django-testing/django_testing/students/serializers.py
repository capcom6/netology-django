from django.conf import settings
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    def validate_students(self, value):
        if len(value) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError(
                f"Cannot add more than {settings.MAX_STUDENTS_PER_COURSE} students to a course."
            )

        return value

    class Meta:
        model = Course
        fields = ("id", "name", "students")
