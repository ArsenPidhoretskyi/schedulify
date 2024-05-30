# Schedulify: Admin Interface

We use [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface#readme)
You can configure it via admin panel or use Optional themes.

## Optional themes

This package ships with optional themes as fixtures, they can be installed using the [loaddata admin command](https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-loaddata). Optional themes are activated on installation.

##### [Django](https://www.djangoproject.com/) theme (default):

Run `python manage.py loaddata admin_interface_theme_django.json`

##### [Bootstrap](http://getbootstrap.com/) theme:

Run `python manage.py loaddata admin_interface_theme_bootstrap.json`

##### [Foundation](http://foundation.zurb.com/) theme:

Run `python manage.py loaddata admin_interface_theme_foundation.json`

##### [U.S. Web Design Standards](https://standards.usa.gov/) theme:

Run `python manage.py loaddata admin_interface_theme_uswds.json`
