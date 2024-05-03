from.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import tokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


    class UserSerializer( serializers.ModelSerializer):
        class Meta:
            model = User
        fields = ("id","username"," email ")


    class MytokenObtainPairSerializer(tokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user ):
            token = super ().get_token (user)

            # These are claims, you can add custom claims
            token["full_name"] = user.profile.full_name
            token["username"] = user.username
            token["email"] = user.email
            token["bio"] = user.profile.bio
            token["image"] = str(user.profile.image)
            token["verified"] = user.profile.verified
            #...

            return  token
        
    class RegisterSerializer(serializers.Models.Serializer):
        password: serializers.CharField(
                write_only=True, required=True, validators=[validate_password] )
        password2 = serializers.CharField(
                write_only=True, required=True)
        
        class Meta:
            model = User
            fields = ("email", "username", "password", "password2")
        
        def validate(self, attrs):
            if attrs [ "password "] != attrs ["password2"]:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't  match."}
                )
            return attrs