from rest_framework import serializers
from accounts.models import UserProfile
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    phone = serializers.CharField()
    photo = serializers.ImageField()
    is_tutor = serializers.BooleanField(default=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2', 'phone', 'photo', 'is_tutor']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"Password": "Passwords must match"})

        user.set_password(password)

        user.save()

        phone = self.validated_data['phone']
        photo = self.validated_data['photo']
        is_tutor = self.validated_data['is_tutor']

        profile = UserProfile(user=user, phone=phone, photo=photo, is_tutor=is_tutor)
        profile.save()

        return user


class AccountPropertiesSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField('get_phone_from_user')
    is_tutor = serializers.SerializerMethodField('get_is_tutor_from_user')
    joined_date = serializers.SerializerMethodField('get_joined_date_from_user')
    photo = serializers.SerializerMethodField('get_photo_from_user')

    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name', 'username', 'phone', 'is_tutor', 'joined_date', 'photo', ]

    def get_phone_from_user(self, user):
        phone = user.profile.phone
        return phone

    def get_is_tutor_from_user(self, user):
        is_tutor = user.profile.is_tutor
        return is_tutor

    def get_joined_date_from_user(self, user):
        joined_date = user.profile.joined_date
        return joined_date

    def get_photo_from_user(self, user):
        photo = user.profile.photo.url
        return photo


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['photo', 'phone', 'is_tutor', ]
