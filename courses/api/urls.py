from django.urls import path
from courses.api.views import (
    api_detail_course_view,
    api_update_course_view,
    api_create_course_view,
    api_delete_course_view,
    ApiCourseListView, )


app_name = 'courses'

urlpatterns = [
    path('create', api_create_course_view, name='create'),
    path('list', ApiCourseListView.as_view(), name='list'),
    path('<slug>', api_detail_course_view, name='details'),
    path('<slug>/update', api_update_course_view, name='update'),
    path('<slug>/delete', api_delete_course_view, name='delete'),
]