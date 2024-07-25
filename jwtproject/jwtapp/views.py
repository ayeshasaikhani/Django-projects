from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserListSerializer, FileSerializer
from .models import CustomUser



class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    #permission_classes = [permissions.IsAdminUser]




class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)




from .models import UploadedFile
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import FileSerializer

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        files = UploadedFile.objects.filter(user=request.user)
        print("Files found:", files)
        page = self.paginate_queryset(files)
        if page is not None:
            serializer = FileSerializer(page, many=True)
            print("Serialized data:", serializer.data)
            return self.get_paginated_response(serializer.data)
        serializer = FileSerializer(files, many=True)
        print("Serialized data:", serializer.data)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.no_of_files_uploaded >= 3:
            return Response({'error': 'File upload limit reached'}, status=status.HTTP_400_BAD_REQUEST)
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(user=request.user)
            request.user.no_of_files_uploaded += 1
            request.user.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        file_id = request.data.get('id')
        file_instance = UploadedFile.objects.get(id=file_id, user=request.user)
        file_serializer = FileSerializer(instance=file_instance, data=request.data, partial=True)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        file_id = request.data.get('id')
        print("file_id", file_id)
        file_instance = UploadedFile.objects.get(id=file_id, user=request.user)
        file_instance.delete()
        request.user.no_of_files_uploaded -= 1
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    





