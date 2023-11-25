from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TodoSerializer
from .models import Todo
from rest_framework.views import APIView
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
    def get(self, request):
        todo_objs = Todo.objects.all()
        serializer = TodoSerializer(todo_objs, many=True)

        return Response({
            'status': 200,
            'message': 'fetched successfuly',
            'data': serializer.data
        })

    def post(self, request):
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
