from rest_framework import serializers


class UserNameSerializer(serializers.Serializer):
    title = serializers.CharField()
    first = serializers.CharField()
    last = serializers.CharField()


class UserCoordinatesSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=10, decimal_places=8)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=8)


class UserTimezoneSerializer(serializers.Serializer):
    offset = serializers.CharField()
    description = serializers.CharField()


class UserLocationSerializer(serializers.Serializer):
    street = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    postcode = serializers.IntegerField()
    coordinates = UserCoordinatesSerializer()
    timezone = UserTimezoneSerializer()


class UserDateOfBirthSerializer(serializers.Serializer):
    date = serializers.DateTimeField()


class UserRegisteredSerializer(serializers.Serializer):
    date = serializers.DateTimeField()


class UserPictureSerializer(serializers.Serializer):
    large = serializers.URLField()
    medium = serializers.URLField()
    thumbnail = serializers.URLField()


class UserModelSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=["M", "F", "O"])
    name = UserNameSerializer()
    location = UserLocationSerializer()
    email = serializers.EmailField()
    dob = UserDateOfBirthSerializer()
    registered = UserRegisteredSerializer()
    telephoneNumbers = serializers.ListField(
        child=serializers.CharField(), source="phone"
    )
    mobileNumbers = serializers.ListField(child=serializers.CharField(), source="cell")
    picture = UserPictureSerializer()
