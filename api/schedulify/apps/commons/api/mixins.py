from rest_framework.serializers import Serializer


class MultiSerializerMixin:
    @property
    def _action(self):
        action = getattr(self, "action", None)
        if action is None:
            raise AttributeError("MultiSerializerMixin should be used with ViewSet.")
        return action

    @property
    def _serializer_class(self):
        serializer_class = getattr(self, "serializer_class", None)
        if serializer_class is None:
            raise AttributeError("You must define a serializer_class attribute in the ViewSet.")
        return serializer_class

    @property
    def _serializer_classes(self):
        serializer_classes = getattr(self, "serializer_classes", None)
        if serializer_classes is None:
            raise AttributeError("You must define a serializer_classes attribute in the ViewSet.")
        return serializer_classes

    def get_serializer_class(self) -> Serializer:
        return self._serializer_classes.get(self._action, self._serializer_class)
