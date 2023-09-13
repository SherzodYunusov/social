from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'

class ProgramsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Programs
        fields = '__all__'
        depth = 1

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

class KodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kod
        fields = '__all__'

class PasswordSerializer(serializers.ModelSerializer):
    apps = ProgramsSerializer(many=True, read_only=True)
    class Meta:
        model = Password
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
