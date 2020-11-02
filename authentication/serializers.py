from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):


    confirm_password = serializers.CharField(allow_blank = True, allow_null = True)


    def create(self, validated_data):


        if not validated_data.get("confirm_password", None):

            raise serializers.ValidationError({"confirm_password": "This field is required."})



        confirm_password = validated_data.pop("confirm_password")

        if confirm_password != validated_data["password"]:

            raise serializers.ValidationError({"non_field_errors": "Confirm password and password must match."})


        return User.objects.create_user(**validated_data)


    def update(self, instance, validated_data):

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()

        if validated_data.get("confirm_password") and validated_data.get("password"):

            if validated_data["confirm_password"] != validated_data["password"]:

                raise serializers.ValidationError({"non_field_errors": "Confirm password and password must match."})

            instance.set_password(validated_data["password"])

            instance.save()

            

        return instance

    
    class Meta:

        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name", "password", "confirm_password"
        )
        extra_kwargs = {
            "password":{
                "write_only": True
            },
            "confirm_password":{
                "write_only": True
            }
        }