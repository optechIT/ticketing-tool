from rest_framework import serializers
from .models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'is_staff',
            'is_superuser',
            'created_at',
            'updated_at'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone_no',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # 🔒 hash password
        user.save()
        return user
    

class UserDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only= True)
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        # Remove password if present → prevents update
        validated_data.pop('password', None)
        return super().update(instance, validated_data)