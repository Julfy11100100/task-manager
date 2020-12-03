from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"User was registered successfully"}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
