import random

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_courses_retrieve(api_client, course_factory):
    course = course_factory()
    url = reverse("courses-detail", kwargs={"pk": course.id})

    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert_course(data, course)


@pytest.mark.django_db
def test_courses_list(api_client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse("courses-list")

    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert len(data) == len(courses)

    for i, m in enumerate(data):
        assert_course(m, courses[i])


@pytest.mark.django_db
def test_courses_list_filter_by_id(api_client, course_factory):
    courses = course_factory(_quantity=10)
    course = random.choice(courses)
    url = reverse("courses-list")

    resp = api_client.get(url, data={"id": course.id})
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert len(data) == 1

    assert_course(data[0], course)


@pytest.mark.django_db
def test_courses_list_filter_by_name(api_client, course_factory):
    courses = course_factory(_quantity=10)
    course = random.choice(courses)
    url = reverse("courses-list")

    resp = api_client.get(url, data={"name": course.name})
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert len(data) == 1

    assert_course(data[0], course)


@pytest.mark.django_db
def test_courses_create(api_client):
    data = {"name": baker.random_gen.gen_string(36)}
    courses_count = Course.objects.count()
    url = reverse("courses-list")

    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    assert Course.objects.count() == courses_count + 1


@pytest.mark.django_db
def test_courses_update(api_client, course_factory):
    course = course_factory()
    data = {"name": baker.random_gen.gen_string(36)}
    url = reverse("courses-detail", kwargs={"pk": course.id})

    response = api_client.patch(url, data=data)
    assert response.status_code == status.HTTP_200_OK

    patched_course = Course.objects.get(pk=course.pk)
    assert patched_course.name == data["name"]


@pytest.mark.django_db
def test_courses_delete(api_client, course_factory):
    courses = course_factory(_quantity=10)
    course = random.choice(courses)
    url = reverse("courses-detail", kwargs={"pk": course.id})

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert Course.objects.count() == len(courses) - 1


@pytest.mark.parametrize(
    ["limit", "status_code"],
    [
        (1, status.HTTP_400_BAD_REQUEST),
        (2, status.HTTP_201_CREATED),
        (3, status.HTTP_201_CREATED),
    ],
)
@pytest.mark.django_db
def test_courses_students_limit_failure(
    api_client, student_factory, settings, limit, status_code
):
    settings.MAX_STUDENTS_PER_COURSE = limit
    students = student_factory(_quantity=2)
    data = {
        "name": baker.random_gen.gen_string(36),
        "students": [s.id for s in students],
    }
    url = reverse("courses-list")

    response = api_client.post(url, data=data)
    assert response.status_code == status_code


def assert_course(data, course):
    assert data["id"] == course.id
    assert data["name"] == course.name
