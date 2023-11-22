from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TodoSerializer

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
        print(data, 'data')
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            return Response({
                "status": 200,
                'message': 'Data is added successfully'
            })
        else:
            return Response({
                "status": 422,
                'message': 'Invalid configurations',
                "data": serializer.errors
            })

    except Exception as e:
        print(e)
