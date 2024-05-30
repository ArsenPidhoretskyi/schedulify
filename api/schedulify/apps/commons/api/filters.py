from rest_framework.filters import OrderingFilter


class SwaggerOrderingFilter(OrderingFilter):
    def __get_ordering_choices(self, view) -> list:
        return [
            f"{ordering}{field}"
            for field, _ in self.get_valid_fields(view.get_queryset(), view, {})
            for ordering in ["", "-"]
        ]

    def get_schema_operation_parameters(self, view):
        parameters = super().get_schema_operation_parameters(view)
        parameters[0]["schema"]["enum"] = self.__get_ordering_choices(view)
        return parameters
