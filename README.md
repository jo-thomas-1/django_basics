# Django Basics

Django is a free and open-source, Python-based web framework that follows the model–template–views architectural pattern. It is maintained by the Django Software Foundation, an independent organization established in the US as a 501 non-profit.

Model-View-Template, sometimes also referred to as MTV(Model-Template-View) is a design pattern or design architecture that Django follows to develop web applications. It is slightly different from the commonly known MVC(Model-View-Controller) design pattern.

- the python package `virtualenvwrapper-win` can be used to create virtual environments for the project
- open command window in main folder and execute `mkvirtualenv [environment_name]`
- if the created virtual environment is not automatially opened use command `workon [environment_name]`
- in windows, the `lsvirtualenv` command can be used to get list of virtual environments in system

- install django using `pip install django`
- to get any specific version use `pip install django==[version]`

- to create a project inside the main environment folder run the command `django-admin startproject [project_name]`
- adding a `.` at the end will tell django to use the current directory as the project folder

- to run the created application in django server use command `python manage.py runserver`
- once this command is executed, check if the command line shows that there are any unapplied migrations
- if there are, then stop the server and execute `python manage.py migrate`
- the expected message when server is started is `System check identified no issues`

## App

An app is a web application that does something – e.g., a blog system, a database of public records or a small poll app. A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.

- to create an app use code `python manage.py startapp [app_name]`
- add the app name `[app_name]` in the `INSTALLED_APPS` list in `settings.py` file of project

## View

- views are basically the content that is send in response to a request
- in the app folder go to `views.py` and create function for the view required
- this function will take an http request and send the content as response
- so import the http response package `from django.http import HttpResponse`

```
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):
	return HttpResponse("<h1>Hello World</h1>")
```

- as everything works based on http request and response, it is important to create urls that maps to every view
- in th app folder create a file `urls.py`
- here map all views to urls as needed
- the mapping must be done in a list with the name `urlpatterns` as django looks for the same

```
from django.urls import path
from . import views # importing views module from current folder

urlpatterns = [
    path('', views.hello_world, name='test_app_hello')
]
```

## URL's

- now this configuration needs to be linked to the main project urls
- add app urls to the `urlpatterns` in `urls.py` in main project folder
- as this is another url configuration, just as mentioned in the documentation
	- import the include() function: from django.urls import include, path
    - add a URL to urlpatterns:  path('blog/', include('blog.urls'))

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('test_app.urls'))
]
```

Now the main project is linked to urls in test_app via `path('', include('test_app.urls'))`, then from test_app urls it is liked to the corresponding view via `path('', views.hello_world, name='test_app_hello')`.

## Template

A template is basically an HTML file which is to be rendered by the view functions.

- templates are created and stored as normal html files by creating a folder named `templates` inside the corresponding app folder
- django can auto detect these files as the name `templates` is a part of the file structure
- if the template is not specific to any particular app, the `templates` folder can also be placed in the root folder of project
- if the templates are being created in any location other than inside specific app folders, the path must be added to `DIRS` list in the `TEMPLATES` list in `settings.py` file in main project folder
- to provide path, import the os package in `settings.py` and impliment `[os.path.join(BASE_DIR, 'folder_name_or_path')]`

- once the template files are created they can be rendered to the site using the render function

```
def hello_world(request):
	return render(request, 'hello.html')
```

## Passing Values

- this is used to place dynamic/calculated content in the page
- it is done through the view functions in `views.py` file of each app
- the required values are passed as a third argument in the render function in dictionary format
- eg: `render(request, 'hello.html', {'key': value})`
- Jinja is the default template engine to mark the placeholder in the template html file
- eg: `<h2>This is a template page - {{key}} - with the placeholder</h2>`

```
def hello_world(request):
    keyword = "tester"
    return render(request, 'hello.html', {'keyword': keyword})
```

### Passing values to another page

- add html code that transferes values to other pages. for example a form.
- for action attribute, a url is provided, not direct html page path

```
<form method="GET" action="add">
    <input type="text" name="num_one">
    <input type="text" name="num_two">
    <input type="submit">
</form>
```

- add the view function to handle the specified path
- this can be with the HttpResponse or render functions as required
- read the passed values with GET or POST parameters

```
def pass_value(request):
    value_1 = int(request.GET['num_one'])
    value_2 = int(request.GET['num_two'])

    return render(request, 'hello.html', {'keyword': value_1 + value_2})
```

- update the path to `urls.py` - `path('add', views.pass_value, name='test_app_pass_value')`

## Static Files / Assets

All elements used in the website, like images, css, js scripts, fonts, etc. are refreed to as assets or static files. As they do not need to be processed in any way, they can just be served up as is. They are also much easier to cache.

- these static files need to be properly linked in the django file structure
- make sure that `django.contrib.staticfiles` is included in INSTALLED_APPS list in `settings.py`
- in your settings file also define or update the value of `STATIC_URL` as required

```
STATIC_URL = 'static/'
```

- in the templates, use the static template tags to provide relative paths to required files from root static directory

```
{% load static %}
<img src="{% static 'relative_path/example.jpg' %}" alt="My image">
```

- make sure that the static files are all stored in a folder called `static` in corresponding app folder
- just as in the case of templates, if the assets are not specific to any particular app, the `static` folder can also be placed in the root folder of project
- in this case or if the static folder is being placed in any other location, the path must be added to `STATICFILES_DIRS` list in the `settings.py` file in main project folder

```
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

- `STATIC_ROOT` is the absolute path to the directory where django will collect static files for deployment
- the command `python manage.py collectstatic` will copy all the static files(i.e. in static folder in apps, static files in all paths) to the `STATIC_ROOT` directory

- `MEDIA_URL` and `MEDIA_ROOT` have the same purpose just as `STATIC_URL` and `STATIC_ROOT`, but for media contents in our project. These are files that a user uploads.

- media files need to be treated separately because
    - files uploaded by end-users may be harmfull and so cannot be trusted
    - files may need to perform processing to be served better (for example, uploaded images may need to be optimized to support different devices)
    - user uploaded file may replace a static file accidentally

- it is also better to provide the debug settings when setting up the static folder
- for this the code is provided in the `urls.py` file in the project folder

```
from django.conf.urls.static import static
from static_site_one import settings

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Model

A Django model is the built-in feature that Django uses to create tables, their fields, and various constraints. It is a Python class that inherits from the Model class. Django web applications access and manage data through these Python objects. SQL (Structured Query Language) is complex and involves a lot of different queries for creating, deleting, updating or any other stuff related to database. Django models simplify the tasks and organize tables into models. Generally, each model maps to a single database table. Models define the structure of stored data, including the field types and possibly also their maximum size, default values, selection list options, help text for documentation, label text for forms, etc.

- each model is a Python class that subclasses `django.db.models.Model`
- each attribute of the model represents a database field
- Django provides an automatically-generated database-access API

---

- the tables to store data are created in the `models.py` file in the specific app folder
- as mentioned above, each model is a Python class that subclasses `django.db.models.Model`
- to create a new model, create class `class [Model_name](models.Model):`
- each entity or coulumn in the table is given as a new variable in this class
- based on requirement, each of them can be set to a specific field type
- specific packages may be needed to be installed to use some field types (for example, image field requires the pillow package)

```
from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='pics')
    desc = models.TextField()
```

- a string function can be added in the class to get displays in preferred mode

```
from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='pics')
    desc = models.TextField()

    def __str__(self):
        return self.name
```

- whenever a change in made in the `models.py` file, before running server run the command,
    - `python manage.py makemigrations` to pack up model changes and prepare to be applied (we can verify this step by checking the new file that has been created in the `migrations` folder)
    - `python manage.py migrate` to apply the changes (make sure to keep the database system on before execution)

- to view the tables in a database system, go to the `DATABASES` list in the `settings.py` file in project folder
- here change the `ENGINE` value to the preferred system (for example, mysql)
- usually the default value is `django.db.backends.sqlite3`
- update the `NAME` value to the preferred database name (a database with the name specified must already be created in the database system) - default value `BASE_DIR / 'db.sqlite3'`
- create new key value pairs to store account credentials

- below is the code for connecting with XAMPP SQL
- `mysqlclient` package will be required here

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_models',
        'USER': 'root',
        'PASSWORD': ''
    }
}
```

- the tables can also be accessed through the django admin panel
- when viewing the database it can be seen that django also automatically creates other tables that may be required by the system

## Admin Panel

- django provides a builtin admin panel
- it reads metadata from your models to provide a quick, model-centric interface where trusted users can manage content on your site
- url to admin panel is by default `admin\` - the same can be checked in the `urls.py` file in project folder
- to set the admin account credentials use command `python manage.py createsuperuser` and provide values as required
- the admin account will have a variety of options by which the project can be modified

- to be able to access project tables, they first need to be connected to the admin panel
- import the created models to the `admin.py` file as `from . models import Model_name`
- the imported models also needs to be registered

```
from django.contrib import admin
from . models import Model_name

# Register your models here.
admin.site.register(Model_name)
```

## Dynamic Data

- to connect the data in the database to website, django uses ORM
- ORM (Object Relational Mapper) is used to send data between a database and models in an application. It maps a relation between the database and a model. So, ORM maps object attributes to fields of a table.
- ORM helps to convert data from a relational database system to object oriented system

- for this first import the models to the views file of the specific app `from . models import Model_name`
- to fetch all the data in model use code `Model_name.objects.all()`
- now the fetched values can be passed to the HTML files via render function

```
from django.shortcuts import render
from . models import Model_name

# Create your views here.

def home(request):
    obj = Model_name.objects.all()

    return render(request, 'index.html', {'key': obj})
```

- make sure to insert placeholders as required
- if media urls have not been set, `.url` must be provided for image objects

```
{% for i in places %}
<div class="col-lg-4">
    <img src="{{ i.image.url }}" alt="">
    <h1 class="">{{ i.name }}</h1>
    <p>{{ i.desc }}</p>
</div>
{% endfor %}
```

## Example Projects

The following are some sample projects created based on the above documentation.

| # | Name | Action |
|---|---|---|
| 1 | Views & Templates | [Go to code](https://github.com/jothomas1996/django-view-template) |
| 2 | URL's | [Go to code](https://github.com/jothomas1996/django-site-urls) |
| 3 | Passing values between pages | [Go to code](https://github.com/jothomas1996/django-pass-value-page) |
| 4 | Static Site | [Go to code](https://github.com/jothomas1996/django-static-site) |
| 5 | Models & Admin Page | [Go to code](https://github.com/jothomas1996/django-models) |