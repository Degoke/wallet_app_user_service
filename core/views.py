from urllib import response
from core.exceptions import BadRequest, InvalidUrl
from core.models import User
from rest_framework import viewsets, status, generics
from core.permissions import IsAnonOrAdmin
from core.serializers import (
    UserSerializer,
    LoginSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException, NotFound, ValidationError

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAnonOrAdmin]

    def create(self, request, user_type):
        user_types = ['user', 'staff']

        if user_type not in user_types:
            raise InvalidUrl()
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']

            if user_type == 'user':
                user = User.objects.create_user(email, password, first_name, last_name)
            elif user_type == 'staff':
                user = User.objects.create_staff(email, password, first_name, last_name)
            
            details = self.get_serializer(user).data
            response_data = {"details": details}
            return Response(response_data)
        else:
            raise BadRequest(details={'detail': serializer.errors})

class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, user_type):
        user_types = ['user', 'staff']

        if user_type not in user_types:
            raise InvalidUrl()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                if user_type == 'user':
                    user = User.objects.get(email=email, is_staff=False)
                elif user_type == 'staff':
                    user = User.objects.get(email=email, is_staff=True)
            except User.DoesNotExist:
                raise NotFound(detail=f"User with email {email} does not exist")
                
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            details = {
                "refresh": str(refresh),
                "access": str(access),
                "user": UserSerializer(user).data
            }

            response_data = {"status": "success", "data": details}

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise BadRequest(details={'detail': serializer.errors})

class GetUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self, user_type):
        if user_type == 'users':
            return User.objects.filter(is_staff=False).order_by('-date_joined')
        elif user_type == 'staffs':
            return User.objects.filter(is_staff=True).order_by('-date_joined')
        

    def list(self, request, user_type):
        user_types = ['users', 'staffs']
        if user_type not in user_types:
            raise InvalidUrl()
        queryset = self.get_queryset(user_type)
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"status": "success", "data": serializer.data}
        return Response(response_data)


class CurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        print(request.META['REMOTE_ADDR'])
        user = request.user
        response_data = {"status": "success", "data": self.get_serializer(user).data}
        return Response(response_data)

