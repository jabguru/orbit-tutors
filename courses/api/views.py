from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter

from courses.api.serializers import CourseSerializer
from courses.models import Course
from django.contrib.auth.models import User


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_course_view(request, slug):

    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_course_view(request, slug):

    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if course.author != user:
        return Response({"Response": "You don't have permission to edit that."})

    if request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)

        data = {}

        if serializer.is_valid():
            serializer.save()
            data['success'] = 'Update successful'
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_course_view(request, slug):

    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if course.author != user:
        return Response({"Response": "You don't have permission to delete that."})

    if request.method == 'DELETE':
        operation = course.delete()
        data = {}

        if operation:
            data["Success"] = "Delete successful"
        else:
            data["Failure"] = "Delete failed"

        return Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_course_view(request):
    account = request.user

    course = Course(author=account)

    if request.method == "POST":
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiCourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter, )
    search_fields = ('title', 'description', 'author__username', )



