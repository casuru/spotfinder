from django.contrib.auth import get_user_model
from rest_framework import viewsets, views, status, response
from authentication.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()


class MeView(views.APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):

        serialized_user = UserSerializer(request.user, context = {'request':request})

        return response.Response(serialized_user.data, status = status.HTTP_200_OK)

    def patch(self, request):

        serialized_user = UserSerializer(request.user, data = request.data, partial = True, context = {'request': request})
        if serialized_user.is_valid():

            serialized_user.save()
            return response.Response(serialized_user.data, status = status.HTTP_200_OK)

        return response.Response(serialized_user.errors, status = status.HTTP_400_BAD_REQUEST)