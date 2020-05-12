# mysite
mysite project from the Django Tutorial with the autorest extension that generates a REST API for all the models of a Django project.
# Release Description
In this release the extension is implemented as a 'pre-view' wrapper, which acts as a view and generates the necessary serializer and viewset classes on the fly upon receiving a request at the assumed API's URL. The extension is distributed as a Test PyPI package.
# Requirements
- Python 3.8.2
- Django 3.0.5
- DRF 3.11.0
# Guide
## Setup
1. ```python -m pip install --index-url https://test.pypi.org/simple autorest-oleg1248==0.0.1```
2. Add ```autorest``` to the list of installed apps:
```
INSTALLED_APPS = [
    ...
    'autorest.apps.AutorestConfig',
    ...
]
```

## Usage
Read the just created REST API with ```http://<host>/<path>/<model_name_plural>?<field_name1>=<value1>&<field_name2>=<value2>&order_by=<field_name_to_order_by>&limit=<max_number_of_objects_to_read>```.

Create an object with a POST request to ```http://<host>/<path>/<model_name_plural>```.

Modify an object with a PUT request to ```http://<host>/<path>/<model_name_plural>/<pk>```.

Delete an object with a DELETE request to ```http://<host>/<path>/<model_name_plural>/<pk>```. 
