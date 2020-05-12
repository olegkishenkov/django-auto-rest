# mysite
mysite project from the Django Tutorial with the autorest extension that generates a REST API for all the models of a Django project.
# Release Description
In this release the extension is implemented as a 'pre-view' wrapper, which acts as a view and generates the necessary serializer and viewset classes on the fly upon receiving a request at the assumed API's URL. The crucial parts of the code are covered with tests. The extension is distributed as a Test PyPI package.
# Requirements
- Python 3.8.2
- Django 3.0.5
- DRF 3.11.0
# Guide
## Setup
1. ```python -m pip install --index-url https://test.pypi.org/simple autorest-oleg1248==0.0.2```
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

# Demonsrtation
The demonstration shows how the ```autorest``` extension is run on the models of the ```polls``` app from the [original Django tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/). First, let's create the project with the app:

```django-admin startproject mysite```

```python manage.py startapp polls```

``` python
# polls/models.py
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
``` python
# myproject/settings.py
INSTALLED_APPS = [
    ...
    'polls.apps.PollsConfig',
    'rest_framework',
    ...
]
```
```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py runserver```

Second, let's install the ```autorest``` extension.

```python -m pip install --index-url https://test.pypi.org/simple autorest-oleg1248==0.0.2```

```
INSTALLED_APPS = [
    ...
    'autorest.apps.AutorestConfig',
    ...
]
```

``` python
# mysite/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('autorest.urls')),
    ...
]
```

Third, let's use the REST API's browser interface to manipulate Question objects as described in the 'Usage' section. If we go to 
```http://127.0.0.1:8000/questions``` we'll see no objects. Let's create two question objects by sending POST requests to the same address:
![Image of the creation of Question objects](https://github.com/oleg1248/mysite/blob/release-onthefly/art/question_create.png)
![Image of the creation of Question objects 1](https://github.com/oleg1248/mysite/blob/release-onthefly/art/question_create_1.png)

Then we can send a GET request to the same address and see the just created objects:
![Image of the just created Question objects](https://github.com/oleg1248/mysite/blob/release-onthefly/art/question_list.png)

Now it's time to retrieve the Question object with the ```id``` 3 by sending a GET request to ```http://127.0.0.1:8000/questions/3```:
![Image of the retrieval of the Question object](https://github.com/oleg1248/mysite/blob/release-onthefly/art/question_retrieve.png)

How about updating the same object by sending a PUT request to the same address?
![Image of the update of the Question object](https://github.com/oleg1248/mysite/blob/release-onthefly/art/question_update.png)

Finally, we can destroy the object by sending a DELETE request to the address, which we've already used three times:
![Image of the destruction of the Question object](https://github.com/oleg1248/mysite/blob/release-onthefly/art/question_destroy.png)