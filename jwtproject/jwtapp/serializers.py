from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password', 'address', 'phone', 'age')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data['address'],
            phone=validated_data['phone'],
            age=validated_data['age']
        )
        return user







class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()





from .models import UploadedFile

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('id', 'file', 'name', 'uploaded_at')





class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone', 'age', 'no_of_files_uploaded', 'created_at']