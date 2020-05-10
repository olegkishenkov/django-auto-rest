# mysite
mysite project from the Django Tutorial with the autorest extension that generates a REST API for all the models of a Django project.
# Guide
## Setup
1. Copy the autorest app directory to the root directory of your Django project;
2. Add ```autorest``` to the ```INSTALLED_APPS```.
## Usage
Run ```manage.py makeapi```

Read the just created REST API with ```http://<host>/<path>/<model_name_plural>?<field_name1>=<value1>&<field_name2>=<value2>&order_by=<field_name_to_order_by>&limit=<max_number_of_objects_to_read>```.

Create an object with a POST request to ```http://<host>/<path>/<model_name_plural>```.

Modify an object with a PUT request to ```http://<host>/<path>/<model_name_plural>/<pk>```.

Delete an object with a DELETE request to ```http://<host>/<path>/<model_name_plural>/<pk>```. 
