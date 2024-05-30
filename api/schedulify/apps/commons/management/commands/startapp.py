import os

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.startapp import Command as StartappCommand


class Command(StartappCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--raw",
            help="Create a raw app without any subdirectories",
            action="store_true",
        )

    @staticmethod
    def __create_packages(directory: str, packages: list):
        for package in packages:
            path = os.path.join(directory, package)
            os.makedirs(path)
            open(os.path.join(path, "__init__.py"), "w").close()

    def handle(self, **options):
        directory = options["directory"]
        if directory is None:
            directory = os.path.join(settings.BASE_DIR, "apps", options["name"])

            try:
                os.makedirs(directory, exist_ok=True)
            except FileExistsError:
                raise CommandError(f"'{directory}' already exists")  # pylint: disable=raise-missing-from

            options["directory"] = directory

        super().handle(**options)

        if options["raw"]:
            return

        api_directory = os.path.join(directory, "api")
        sub_directories = ["admin", "models", "services", "tests", api_directory]
        self.__create_packages(directory, sub_directories)

        v1_api_directory = os.path.join(api_directory, "v1")
        self.__create_packages(api_directory, ["v1"])
        api_sub_directories = ["serializers", "views"]
        self.__create_packages(v1_api_directory, api_sub_directories)

        for urls_path in [api_directory, v1_api_directory]:
            open(os.path.join(urls_path, "urls.py"), "w").close()

        for file_name in ["models.py", "tests.py", "views.py", "admin.py"]:
            os.remove(os.path.join(directory, file_name))
