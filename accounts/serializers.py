from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, data):
        # Check if the password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Check if a user with this username already exists
        if MyUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})

        # Check if a user with this email already exists
        if MyUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        return data

    def create(self, validated_data):
        # Remove confirm_password from validated data since we don't need to store it
        validated_data.pop('confirm_password')

        # Create the user and set the password
        user = MyUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'phone_number']  # Include fields to be displayed
