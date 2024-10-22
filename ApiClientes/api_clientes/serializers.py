from rest_framework.serializers import IntegerField, URLField, CharField
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


class ListOfUsersSerializer(serializers.Serializer):
    users = UserModelSerializer(many=True)


class ResponseSerializer(serializers.Serializer):
    totalCount = IntegerField(read_only=True)
    pageNumber = IntegerField(read_only=True)
    totalPages = IntegerField(read_only=True)
    pageSize = IntegerField(default=10)
    next = URLField(required=False)
    previous = URLField(required=False)
    results = ListOfUsersSerializer()


class MainViewSerializer(serializers.ListSerializer):
    child = URLField()


class RegionsSerializer(serializers.Serializer):
    class RegionSerializer(serializers.ListSerializer):
        child = CharField()

    regions = RegionSerializer(many=True)


class TagsSerializer(serializers.ListSerializer):
    child = CharField()
