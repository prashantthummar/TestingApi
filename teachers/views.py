from django.shortcuts import render
from rest_framework import status, permissions, authentication, views, viewsets
from rest_framework.response import Response
from organizations import models as organizations_models
from django.db.models import Q

# Utils
import json
from utils.decorators import validate_org,validate_dept,is_student,is_teacher, is_organization
from utils.utilities import pop_from_data

from . import models, serializers
from departments import serializers as department_serializers
from subjects import models as subjects_models
from departments import models as department_models
# Swagger
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi


#TODO: get req for teacher
class Teacher(views.APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TeacherSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response("OK- Successful GET Request"),
            401: openapi.Response(
                "Unauthorized- Authentication credentials were not provided. || Token Missing or Session Expired"),
            500: openapi.Response("Internal Server Error- Error while processing the GET Request Function.")
        },
        manual_parameters=[
            openapi.Parameter(name="org_id", in_="query", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        query_params = self.request.query_params
        org_id = query_params.get('org_id', None)

        qs = models.Teacher.objects.filter(is_active=True)

        if org_id:
            qs = qs.filter(organization__org_id=org_id)

        serializer = serializers.TeacherSerializer(qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body = openapi.Schema(
            title = "Join teacher request",
            type=openapi.TYPE_OBJECT,
            properties={
                'org_join_id': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response("OK- Successful POST Request"),
            401: openapi.Response("Unauthorized- Authentication credentials were not provided. || Token Missing or Session Expired"),
            422: openapi.Response("Unprocessable Entity- Make sure that all the required field values are passed"),
            500: openapi.Response("Internal Server Error- Error while processing the POST Request Function.")
        }
    )
    def post(self, request):
        data = json.loads(json.dumps(request.data))
        org_join_id = data.get("org_join_id")

        if not org_join_id:
            errors = [
                'Org_Join_ID  is not passed'
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)

        organizations = organizations_models.Organization.objects.filter(join_id=org_join_id)
        if not len(organizations):
            errors = [
                'Invalid organization Join ID'
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)

        organization = organizations[0]

        if not organization.is_active:
            errors = [
                'Invalid organization Join ID'
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)

        if not organization.accepting_req:
            errors = [
                'This organization is currently not accepting requests'
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)

        data.update({
            "user": request.user.id,
            "requested_organization": organization.id
        })

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body = openapi.Schema(
            title = "Update Teacher",
            type=openapi.TYPE_OBJECT,
            properties={
                'org_id': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_INTEGER),
                'teacher_id': openapi.Schema(type=openapi.TYPE_STRING),

            }
        ),
        responses={
            200: openapi.Response("OK- Successful POST Request"),
            401: openapi.Response("Unauthorized- Authentication credentials were not provided. || Token Missing or Session Expired"),
            422: openapi.Response("Unprocessable Entity- Make sure that all the required field values are passed"),
            500: openapi.Response("Internal Server Error- Error while processing the POST Request Function.")
        }
    )
    @validate_org
    @is_teacher
    def put(self, request, *args, **kwargs):
        data = request.data

        data = pop_from_data(["is_active", "user", "organization"], data)

        teacher = kwargs.get("teacher")

        serializer = serializers.TeacherSerializer(teacher,data=data, partial=True)

        if not serializer.is_valid():
               return Response({'details': [str(serializer.errors)]}, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        msgs = [
            'successfully updated assignment'
        ]
        return Response({'details': msgs}, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            title="Delete Student",
            type=openapi.TYPE_OBJECT,
            properties={
                'org_id': openapi.Schema(type=openapi.TYPE_STRING),
                'teacher_id': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response("OK- Successful POST Request"),
            401: openapi.Response(
                "Unauthorized- Authentication credentials were not provided. || Token Missing or Session Expired"),
            422: openapi.Response("Unprocessable Entity- Make sure that all the required field values are passed"),
            500: openapi.Response("Internal Server Error- Error while processing the POST Request Function.")
        }
    )
    @is_organization
    def delete(self, request, *args, **kwargs):
        data = request.data
        teacher_id = data.get('teacher_id', None)

        org = kwargs.get('organization')
        teachers = models.Teacher.objects.filter(Q(teacher_id=teacher_id) & Q(organization__org_id=org.org_id)& Q(is_active=True))

        if not len(teachers):
            errors = [
                'invalid teacher id'
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)

        teacher = teachers[0]
        teacher.is_active = False
        teacher.save()

        msgs = [
            "Successfully deleted teacher"
        ]
        return Response({'details': msgs}, status.HTTP_200_OK)



class AssignSubject(views.APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body = openapi.Schema(
            title = "Assign subject to teacher",
            type=openapi.TYPE_OBJECT,
            properties={
                'teacher': openapi.Schema(type=openapi.TYPE_INTEGER),
                'subject': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            200: openapi.Response("OK- Successful POST Request"),
            401: openapi.Response("Unauthorized- Authentication credentials were not provided. || Token Missing or Session Expired"),
            422: openapi.Response("Unprocessable Entity- Make sure that all the required field values are passed"),
            500: openapi.Response("Internal Server Error- Error while processing the POST Request Function.")
        }
    )
    def post(self, request):
        data = request.data
        teacher = data.get('teacher', None)
        subject = data.get('subject', None)

        if not teacher or not subject:
            errors = [
                "teacher and subject ID's are required"
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)
        
        subjects = subjects_models.Subject.objects.filter(Q(id=int(subject)) & Q(is_active=True))

        if not len(subjects):
            errors = [
                "Invalid subject id"
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)
        
        subject = subjects[0]

        teachers = models.Teacher.objects.filter(Q(id=int(teacher)) & Q(is_active=True))
        if not len(teachers):
            errors = [
                "Invalid teacher id"
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)
        
        teacher = teachers[0]

        if teacher in subject.teachers.all():
            errors = [
                "this teacher is already assigned to the subject"
            ]
            return Response({'details': errors}, status.HTTP_400_BAD_REQUEST)
            
        subject.teachers.add(teacher)
        subject.save()

        msgs = [
            'successfully assigned subject to the teacher'
        ]
        return Response({'details': msgs}, status.HTTP_200_OK)

