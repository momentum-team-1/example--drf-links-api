from django.shortcuts import render, get_object_or_404
from rest_framework import views, viewsets, permissions, pagination, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import LinkSerializer
from .models import Link
from users.models import User


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.links.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def followed(self, request):
        queryset = Link.objects.filter(
            owner__fans=request.user).order_by('-created_at').all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Link.objects.order_by('-created_at').all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FollowedView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        name_of_user = request.data["user"]
        user_to_follow = User.objects.get(username=name_of_user)
        current_user = request.user
        current_user.followed_users.add(user_to_follow)
        return Response(
            {"followed_user_count": current_user.followed_users.count()})


class DeleteFollowedView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        request.user.followed_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
