from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data["email"], 
                password=validated_data["password"], 
                first_name=validated_data["first_name"], 
                last_name=validated_data["last_name"]
                )
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist: raise serializers.ValidationError("invalid credentials")

        if user.check_password(password):
            return user
        else:
            raise serializers.ValidationError("invalid credentials")