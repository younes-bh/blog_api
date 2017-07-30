from rest_framework.serializers import (
        EmailField,
        CharField,
        ModelSerializer,
        HyperlinkedIdentityField,
        SerializerMethodField,
        ValidationError,
        )
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email address")
    email2 = EmailField(label="Confirm email", write_only=True)
    class Meta :
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs = {
            "password" : {"write_only" : True},

        }

    def validate(self, data):
        # email = data.get("email")
        # user_qs = User.objects.filter(email = email)
        # if user_qs.exists():
        #     raise ValidationError("A user with that email adress already exists.")
        return data

    def validate_email2(self, value):
        data = self.initial_data
        email1 = data.get("email")
        email2 = value
        if email1 != email2 :
            raise ValidationError("Emails must match : email confirmation is not correct.")
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("A user with that email adress already exists.")
        return value

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        user_obj = User(username = username,
                        email = email,
                        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank= True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = EmailField(label="Email address", allow_blank=True, required=False)
    class Meta :
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {
            "password" : {"write_only" : True}
        }

    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        email = data.get("email", None)
        password = data.get("password")
        if not email and not username:
            raise ValidationError("A username or an email is required to login.")
        user_qs = User.objects.filter(
                Q(username = username)|
                Q(email = email)
            ).distinct()
        user_qs = user_qs.exclude(email__isnull = True).exclude(email__iexact='')
        if user_qs.exists() and user_qs.count() == 1:
            user_obj = user_qs.first()
        else:
            raise ValidationError("This username / email is not valid.")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials, please try again.")
        data["token"] = "Some random token"

        return data

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]