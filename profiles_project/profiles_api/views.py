from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from profiles_api import serializers

# Create your views here.


class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer

    """Test API View"""

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods: get, post, put, patch, delete',
            'It is similar to a Django View',
            'Gives you the most control over you app logic',
            'It is mapped manually to URLs'
        ]

        return Response({
            'message': 'Hello!',
            'an_apiview': an_apiview
        })

    def post(self, request):
        """Create a hello message with our name"""
        print("ALFLAG")
        print(request.data)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        """ Patch: update only fields that were provided in the request"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Handle delete of an object"""
        return Response({'method': 'DELETE'})