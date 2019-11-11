from rest_framework import serializers
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'cost', 'featured_image', 'published', 'attachment', 'author']

    def get_username_from_author(self, course):
        author = course.author.username
        return author
