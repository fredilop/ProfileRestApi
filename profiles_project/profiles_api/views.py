from django.shortcuts import render

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.settings import api_settings

from profiles_api import models
from profiles_api import permissions
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


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """(GET) Return hello message"""

        a_viewset = {
            'Uses actions (list, create, retrieve, update, partial_update',
            'Automaticalle maps to URLs using Router',
            'Provides more functionality with less code',
        }

        return Response({
            'message': 'Hello!!',
            'a_viewset': a_viewset,
        })

    def create(self, request):
        """(POST) Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                'message': message,
                'http_method': 'POST',
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        """(GET by ID)Handle getting an object by its ID"""
        return Response({
            'http_method': 'GET'
        })

    def update(self, request, pk=None):
        """(PUT) Handle updating an object"""
        return Response({
            'http_method': 'PUT'
        })

    def partial_update(self, request, pk=None):
        """(PATCH) Updating part of an object"""
        return Response({
            'http_method': 'PATCH'
        })

    def destroy(self, request, pk=None):
        """(DELETE) Handle removing an object"""
        return Response({
            'http_method': 'DELETE'
        })


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileFeedItemViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    # permission_classes = (
    #     permissions.UpdateOwnStatus,
    #     IsAuthenticatedOrReadOnly
    # )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)