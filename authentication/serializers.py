from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):


    confirm_password = serializers.CharField(allow_blank = True, allow_null = True)


    def create(self, validated_data):


        return User.objects.create_user(
            **validated_data
        )


    def update(self, instance, validated_data):

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()

        if validated_data.get("confirm_password") and validated_data.get("password"):

            if validated_data["confirm_password"] == validated_data["password"]:

                instance.set_password(validated_data["password"])

                instance.save()

        return instance

    
    class Meta:

        model = User
        fields = "__all__"