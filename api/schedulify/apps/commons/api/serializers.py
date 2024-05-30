from rest_framework.serializers import Serializer


class CoreSerializer(Serializer):
    def create(self, validated_data):
        raise NotImplementedError("Do not use create directly")

    def update(self, instance, validated_data):
        raise NotImplementedError("Do not use update directly")


class NullSerializer(Serializer):
    pass
