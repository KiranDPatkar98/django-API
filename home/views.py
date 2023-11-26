from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TodoSerializer, TimingTodoSerializer
from .models import Todo, TimingTodo
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.


@api_view(['GET'])
def home(request):
    return Response({
        "status": 200,
        'message': 'This is your first API'
    })


@api_view(['POST'])
def todo_post(request):
    try:
        data = request.data
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                'message': 'Data is added successfully',
                "data": serializer.data
            })
        else:
            return Response({
                "status": 422,
                'message': 'Invalid configurations',
                "data": serializer.errors
            })

    except Exception as e:
        print(e)


@api_view(['GET'])
def get_todo(request):
    todo_objs = Todo.objects.all()
    serializer = TodoSerializer(todo_objs, many=True)

    return Response({
        'status': 200,
        'message': 'fetched successfuly',
        'data': serializer.data
    })


@api_view(['PATCH'])
def patch_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response(
                {
                    'status': 404,
                    'message': 'UID is required'
                }
            )
        obj = Todo.objects.get(uid=data.get('uid'))
        serializer = TodoSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'updated successfuly',
                "data": serializer.data
            })
        else:
            return Response({
                'status': 409,
                'message': 'Invalid data',
            })

    except Exception as e:
        print(e)


# using class based

class Todo_view(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # to get the data based on data
        todo_objs = Todo.objects.filter(user=request.user)
        # todo_objs = Todo.objects.all()
        serializer = TodoSerializer(todo_objs, many=True)

        return Response({
            'status': 200,
            'message': 'fetched successfuly',
            'data': serializer.data
        })

    def post(self, request):

        try:
            data = request.data
            data['user'] = request.user.id
            serializer = TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    'message': 'Data is added successfully',
                    "data": serializer.data
                })
            else:
                return Response({
                    "status": 422,
                    'message': 'Invalid configurations',
                    "data": serializer.errors
                })

        except Exception as e:
            print(e)

    # for patch and put also you can do like this

    def delete(self, request):
        try:
            data = request.data
            todo = Todo.objects.get(uid=data.get('uid'))
            todo.delete()
            return Response(
                {
                    'status': 200,
                    'message': 'Deleted successfuly'
                }
            )
        except Todo.DoesNotExist:
            return Response({'status': 404, 'message': 'Todo not found'})


# API's using view set


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @action(detail=False, methods=['post'])
    def add_date_to_todo(self, request):
        try:
            data = request.data
            serializer = TimingTodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': 200,
                        'message': 'Success',
                        'data': serializer.data
                    }
                )
            else:
                return Response(
                    {
                        "status": 404,
                        'message': 'Invalid data',
                        "data": serializer.errors
                    }
                )
        except Exception as e:
            print(e)

    @action(detail=False, methods=['GET'])
    def get_timing_todo(self, request):
        todo_objs = TimingTodo.objects.all()
        serializer = TimingTodoSerializer(todo_objs, many=True)

        return Response({
            'status': 200,
            'message': 'fetched successfuly',
            'data': serializer.data
        })
