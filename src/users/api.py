# -*- coding: utf-8 -*-
from django.utils import timezone

from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from blogs.models import Blog
from users.permissions import UserPermission
from users.serializers import UserSerializer


class UsersAPI(GenericViewSet):
    permission_classes = (UserPermission,)
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            blog_created = Blog.objects.create(
                user=user,
                title='El blog de ' + user.username,
                created_date=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
