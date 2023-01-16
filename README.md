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

### Class Generic View

- here the views are implimented as classes
- they help to simplify the common tasks performed in django (eg: actions performed on database)

#### List View

- used to list out or display all records
- in views file import `ListView` as `from django.views.generic import ListView`
- import the related model

```
from django.views.generic import ListView
from . model import Model_name

class TaskListView(ListView):
    model = Model_name
    template_name = 'home.html'
    context_object_name = 'data_set' # name of variable used to pass data to template
```

- link the class in `urls.py`

```
path('cbv/', views.TaskListView.as_view(), name='class_based_list_view')
```

- the html template file is exactly the same
- below is a sample of the above

```
# views.py

from django.views.generic import ListView
from . models import Task

class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
```

```
# urls.py

from django.urls import path
from . import views # importing views module from current folder

app_name = "todo_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('cbvhome/', views.TaskListView.as_view(), name='class_based_list_view')
]
```

```
<!-- home.html -->

{% extends 'base.html' %}
{% block body %}
<div class="container">
    <div class="row">
        <div class="col-6">
            {% for i in tasks %}
            <div class="card shadow mb-2" style="width: 80%;">
                <div class="card-body">
                    <h5 class="card-title">{{ i.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Priority {{ i.priority }}</h6>
                    <p class="card-text">{{ i.date }}</p>
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'todo_app:delete' i.id %}" class="card-link btn btn-danger">Done</a>
                        <a href="{% url 'todo_app:edit' i.id %}" class="card-link btn btn-warning">Update</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

#### Detail View

- used to display specific record in detail
- in views file import `DetailView` as `from django.views.generic.detail import DetailView`
- import the related model

```
from django.views.generic.detail import DetailView
from . model import Model_name

class TaskDetailView(DetailView):
    model = Model_name
    template_name = 'home.html'
    context_object_name = 'data_set' # name of variable used to pass data to template
```

- link the class in `urls.py`
- here name of variable used to passed the id must be given as `pk`
- it stands for primary key
- if not given as `pk`, the system throws an AttributeError `Generic detail view TaskDetailView must be called with either an object pk or a slug in the URLconf.`

```
path('cbvdetail/<int:pk>', views.TaskDetailView.as_view(), name='class_based_detail_view')
```

- below is a sample for the above stated

```
# views.py

from django.views.generic.detail import DetailView
from . models import Task

class TaskDetailView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'
```

```
from django.urls import path
from . import views # importing views module from current folder

app_name = "todo_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('cbvhome/', views.TaskListView.as_view(), name='class_based_list_view'),
    path('cbvdetail/<int:pk>', views.TaskDetailView.as_view(), name='class_based_detail_view')
]
```

```
<!-- detail.html -->

{% extends 'base.html' %}
{% block body %}
<div class="container">
    <h1>Task in details</h1>
    <p><b>Name:</b> {{ task.name }}</p>
    <p><b>Priority:</b> {{ task.priority }}</p>
    <p><b>Date:</b> {{ task.date }}</p>
    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
        <a href="{% url 'todo_app:delete' i.id %}" class="card-link btn btn-danger">Done</a>
        <a href="{% url 'todo_app:edit' i.id %}" class="card-link btn btn-warning">Update</a>
    </div>
</div>
{% endblock %}
```

#### Update View

- used to update specific record
- in views file import `UpdateView` as `from django.views.generic.edit import UpdateView`
- import the related model
- `reverse_lazy()` function is used to redirect once update is successfull
- for this import `reverse_lazy` as `from django.urls import reverse_lazy`
- if a namespace / app_name has been set up in the app's urls.py, then include the namespace when reversing - `reverse('myapp:my_url_name')`

```
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from . model import Model_name

class TaskUpdateView(UpdateView):
    model = Model_name
    template_name = 'update.html'
    context_object_name = 'data_set' # name of variable used to pass data to template
    fields = ['key_1', 'key_2', 'key_3', ...] # names of the fields to be updated

    def get_success_url(self):
        # used to set desitination to go to when the update is successfull
        return reverse_lazy('myapp:my_url_name', kwargs={'pk': self.object.id})
```

- link the class in `urls.py`
- here name of variable used to passed the id must be given as `pk`

```
path('cbvupdate/<int:pk>', views.TaskUpdateView.as_view(), name='class_based_update_view')
```

- below is a sample for the above stated

```
# views.py

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from . model import Task

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ['name', 'priority', 'date']

    def get_success_url(self):
        return reverse_lazy('todo_app:class_based_detail_view', kwargs={'pk': self.object.id})
```

```
from django.urls import path
from . import views # importing views module from current folder

app_name = "todo_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('cbvhome/', views.TaskListView.as_view(), name='class_based_list_view'),
    path('cbvdetail/<int:pk>', views.TaskDetailView.as_view(), name='class_based_detail_view'),
    path('cbvupdate/<int:pk>', views.TaskUpdateView.as_view(), name='class_based_update_view')
]
```

```
<!-- update.html -->

{% extends 'base.html' %}
{% block body %}
    <div class="container mt-3">
        <h2 class="mb-3">Edit Task</h2>

        <form class="mb-3" method="POST" action="">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
{% endblock %}
```

#### Delete View

- used to delete a specific record
- import for `DeleteView` is the same as `UpdateView`, that is `from django.views.generic.edit import DeleteView`
- import the related model

```
from django.views.generic.edit import DeleteView
from . model import Model_name

class TaskDeleteView(DeleteView):
    model = Model_name
    template_name = 'delete.html'
    context_object_name = 'data_set' # name of variable used to pass data to template
    success_url = reverse_lazy('todo_app:class_based_list_view')
```

- link the class in `urls.py`
- here name of variable used to passed the id must be given as `pk`

```
path('cbvdelete/<int:pk>', views.TaskDeleteView.as_view(), name='class_based_delete_view')
```

- below is a sample for the above stated

```
# views.py

from django.views.generic.edit import UpdateView, DeleteView

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('todo_app:class_based_list_view')
```

```
from django.urls import path
from . import views # importing views module from current folder

app_name = "todo_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('cbvhome/', views.TaskListView.as_view(), name='class_based_list_view'),
    path('cbvdetail/<int:pk>', views.TaskDetailView.as_view(), name='class_based_detail_view'),
    path('cbvupdate/<int:pk>', views.TaskUpdateView.as_view(), name='class_based_update_view'),
    path('cbvdelete/<int:pk>', views.TaskDeleteView.as_view(), name='class_based_delete_view')
]
```

```
<!-- delete.html -->

{% extends 'base.html' %}
{% block body %}
    <div class="container mt-3">
        <h2 class="mb-3">Mark task as done</h2>

        <form class="mb-3" method="POST" action="">
            {% csrf_token %}
            <div class="row mb-3">
                <div class="col-sm-10">
                    Are you sure you want to mark this task as completed?
                </div>
            </div>
            <div class="row">
                <div class="col-sm-10">
                    <p><b>Task:</b> {{ task.name }} [Priority {{ task.priority }}]</p>
                </div>
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button type="submit" class="btn btn-danger">Yes</button>
                <a class="btn btn-primary" href="/" role="button">No</a>
            </div>
        </form>
    </div>
{% endblock %}
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

### Base Template

- Django provides the option of a base template
- this base framework can then to implimented to all other pages as needed
- the html pages where the same basic format is required, will be extended from this base template
- first create a base template html file (eg: base.html)
- use placeholders to specify where other blocks/contents will be placed

```
<!DOCTYPE html>
<html lang="en">
    {% load static %}
    <head>
        <meta charset="UTF-8">
        <title>Movie App</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="{% static 'css/main.css' %}">
    </head>
    <body>
        <nav class="navbar">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Features</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Pricing</a>
                </li>
            </ul>
        </nav>

        {% block body %}
            <!-- blocks specified as 'body' will be placed here -->
        {% endblock %}
    </body>
</html>
```

- extend this template in all the new HTML files where this same base format is required

```
{% extends 'base.html' %}
{% block body %}
    <h1>Heading</h1>
    <!-- all elements as required -->
{% endblock %}
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

### Passing values in URL

- placeholders can be used in url's in situations where the users input in not fixed
- in the below example, when user enters the url, any value can be given after `movie/`
- this value can be passed to the corresponding view function as an argument

```
path('movie/<int:movie_id>', views.details, name='details')
```

```
def details(request, movie_id):
    return render(request, 'details.html')
```

- hyperlinks to this page in basic form is as follows

```
<a href="movie/{{ i.id }}"><h3 class="">{{ i.name }}</h3></a>
```

- however, the url must be specified in the below formt using the name given for the url

```
<a href="{% url 'details' i.id %}"><h3 class="">{{ i.name }}</h3></a>
```

- namespaces are used along with the same to avoid confusion
- they are registered in the `urls.py` file of the corresponding app as the variable `app_name`

```
<a href="{% url 'movieapp:details' i.id %}"><h3 class="">{{ i.name }}</h3></a>
```

```
from django.urls import path
from . import views # importing views module from current folder

app_name = "movieapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>', views.details, name='details')
]
```

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

- to read a specific data from the database, the get function can be used

```
obj = Model_name.objects.get(preferred_key_name=preferred_id)
```

## Account Handling

- a combination of steps mentioned in the sections of models and admin panel is used to set this up
- creating a new database is not necessary as django automatically creates a `auth_user` table
- create a registration form in the app HTML page
- for forms with POST method a CSRF (Cross Site Request Forgery) token is required - place the token `{% csrf_token %}` at the start of the form

```
<form method="POST" action="">
    {% csrf_token %}
    <input type="text" name="first_name" placeholder="First Name">
    <input type="text" name="last_name" placeholder="Last Name">
    <input type="text" name="username" placeholder="Username">
    <input type="email" name="email" placeholder="Email">
    <input type="password" name="password" placeholder="Password">
    <input type="password" name="conf_password" placeholder="Confirm Password">
    <input type="submit" name="submit" value="Register">
</form>
```

- the already existing user data in `auth_user` table can be viewed through the linked datbase system or via django admin page
- update the function in `views.py` to handle incoming form data
- once the form data is recieved, execute input validations and register data to the database using `User.objects.create_user()` function
- the parameters of this function are simply the column headings of the `auth_user` table

```
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']

        # validate password and confirm password
        if password == conf_password:
            # check if username already exists
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username " + username + " is already taken")
                return redirect('register')
            # check if email already exists
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                messages.info(request, "Account for " + first_name + " has been registered")
                return redirect('register')
        else:
            messages.info(request, "Password and confirm password fields do no match")
            return redirect('register')

    return render(request, 'register.html')
```

- iterate through messages to view them on the HTML page

```
{% for msg in messages %}
    <h4>{{ msg }}</h4>
{% endfor %}
```

### Account Login

- create corresponding HTML files, views and urls for the login page

```
<form method="POST" action="#">
    {% csrf_token %}
    <input type="text" name="username" placeholder="Username">
    <br><br>
    <input type="password" name="password" placeholder="Password">
    <br><br>
    <input type="submit" name="submit" value="Login">
</form>
{% for msg in messages %}
<h4>{{ msg }}</h4>
{% endfor %}
```
- impliment authentication fnctionality in views

```
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.shortcuts import redirect

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        user.save()

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')
```

- the `is_authenticated` menthod can be used to check if login authentication has been done and make changes accordingly

```
<hr>
{% if user.is_authenticated %}
<h4>Hello {{ user.username }}</h4>
<a href="/account/logout/">Logout</a>
{% else %}
<a href="account/register/">Register</a>
<a href="/account/login/">Login</a>
{% endif %}
<hr>
```

### Account Logout

- create corresponding function in views for logout

```
def logout(request):
    auth.logout(request)
    return redirect('/')
```

- link the function to urls

```
from django.urls import path
from . import views # importing views module from current folder

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
```

- make necessary updates to other contents

```
<hr>
{% if user.is_authenticated %}
<h4>Hello {{ user.username }}</h4>
<a href="/account/logout/">Logout</a>
{% else %}
<a href="account/register/">Register</a>
<a href="/account/login/">Login</a>
{% endif %}
<hr>
```

## CRUD Operations

- creating, reading, updating and deleting data in database

### Create / Add New Data

- create the HTML file with the form to accept data from user

```
<div class="container mt-3">
    <h2 class="mb-3">Add Movie</h2>

    <form class="mb-3" method="POST" action="" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="row mb-3">
            <label for="name" class="col-sm-2 col-form-label">Name</label>
            <div class="col-sm-10">
                <input type="text" class="form-control" name="name" id="name">
            </div>
        </div>
        <div class="row mb-3">
            <label for="year" class="col-sm-2 col-form-label">Year</label>
            <div class="col-sm-10">
                <input type="text" class="form-control" name="year" id="year">
            </div>
        </div>
        <div class="row mb-3">
            <label for="image" class="col-sm-2 col-form-label">Poster</label>
            <div class="col-sm-10">
                <input type="file" class="form-control" name="image" id="image">
            </div>
        </div>
        <div class="row mb-3">
            <label for="desc" class="col-sm-2 col-form-label">Description</label>
            <div class="col-sm-10">
                <textarea class="form-control" name="desc" id="desc" rows="4"></textarea>
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</div>
<div class="container">
    <div>
        {% for msg in messages %}
            <h4>{{ msg }}</h4>
        {% endfor %}
    </div>
</div>
```

- create view function to accept data and store to database

```
def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image']
        year = request.POST['year']
        desc = request.POST['desc']

        movie = Movie(name=name, image=image, year=year, desc=desc)
        movie.save()

        messages.info(request, "Movie has been added to database")

        return redirect('/add')

    return render(request, 'add.html')
```

### Read Data

- as mentioned in the above sections, the `get()` method is used to read data from database and pass onto the template for display
- in the view function first import the relavent models as required as `from . models import Model_name`
- to read all records, use `Model_name.objects.all()`
- to read a specific record or filter out a set of records, provide the search values as arguments to get method as `Model_name.objects.get(key_1=value, key_2=value, ...)`
- update urls to link to corresponding page
- create HTML files with placeholders to display data

```
from django.shortcuts import render
from . models import Movie

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})

def details(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'details.html', {'movie': movie})
```

### Update Data

- Update function is just a modification of the create function
- the required record is read from database and then written back with updated values

```
def update(request, movie_id):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image']
        year = request.POST['year']
        desc = request.POST['desc']

        movie = Movie.objects.get(id=movie_id)
        movie.name = name
        movie.image = image
        movie.year = year
        movie.desc = desc
        movie.save()

        messages.info(request, "Movie has been updated")

        return redirect('/update')

    return render(request, 'update.html')
```

- for the above function to be implimented, an HTML file with the corresponding form needs to be created

```
{% extends 'base.html' %}
{% block body %}
    <div class="container mt-3">
        <h2 class="mb-3">Edit Movie</h2>

        <form class="mb-3" method="POST" action="" enctype="multipart/form-data">
            {% csrf_token %}
            <div class="row mb-3">
                <label for="name" class="col-sm-2 col-form-label">Name</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" name="name" id="name">
                </div>
            </div>
            <div class="row mb-3">
                <label for="year" class="col-sm-2 col-form-label">Year</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" name="year" id="year">
                </div>
            </div>
            <div class="row mb-3">
                <label for="image" class="col-sm-2 col-form-label">Poster</label>
                <div class="col-sm-10">
                    <input type="file" class="form-control" name="image" id="image">
                </div>
            </div>
            <div class="row mb-3">
                <label for="desc" class="col-sm-2 col-form-label">Description</label>
                <div class="col-sm-10">
                    <textarea class="form-control" name="desc" id="desc" rows="4"></textarea>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
{% endblock %}
```

### Delete Data

- the required data is read from the database and then the instance is deleted using the `delete()` method

```
def delete(request, movie_id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=movie_id)
        movie.delete()
        return redirect('/')

    return render(request, 'delete.html')
```

- the corresponding HTML code for getting confirmation from user for deletion is as given below

```
{% extends 'base.html' %}
{% block body %}
    <div class="container mt-3">
        <h2 class="mb-3">Delete Movie</h2>

        <form class="mb-3" method="POST" action="" enctype="multipart/form-data">
            {% csrf_token %}
            Are you sure you want to delete this movie
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button type="submit" class="btn btn-danger">Yes</button>
                <a class="btn btn-primary" href="/" role="button">No</a>
            </div>
        </form>
    </div>
{% endblock %}
```

## Forms

The Django Form class is a feture by which forms can be generated and added to the application. A Django model describes the logical structure of an object, its behavior, and the way its parts are represented to us, a Django Form class describes a form and determines how it works and appears.

A form’s fields are themselves classes; they manage form data and perform validation when a form is submitted. A form field is represented to a user in the browser as an HTML "widget" - a piece of user interface machinery. Each field type has an appropriate default Widget class, but these can be overridden as required.

- the django form class can be used to generate forms based on models
- more specifically, the `ModelForm` class is used as the form is being created using a model as the base
- just as a model class’s fields map to database fields, a form class’s fields map to HTML form `<input>` elements
- in the corresponding app, create a file `forms.py` and initialize the form

```
from django import forms
from . models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'image', 'desc', 'year'] # fields of the model that are required in the form
```

- create the corresponding view function

```
from . models import Movie
from . forms import MovieForm

def edit(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    form = MovieForm(request.POST or None, request.FILES, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'edit.html', {'form': form, 'movie': movie})
```

- create corresponding HTML file to render the form as required
- as it is based on the model, the form will only have fields matching the fields of the model
- the form class does not generate the `form` tag and submit button
- submit button for the form must be created at the end
- it only generates code for the fields as required, all other parent, child or sibling elements must be manually created as required

```
{% extends 'base.html' %}
{% block body %}
    <div class="container mt-3">
        <h2 class="mb-3">Edit Movie</h2>

        <form class="mb-3" method="POST" action="" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
{% endblock %}
```

- django offers many options to modify and render this form to obtain what is required
- some basic reder modes are as below,
    - `{{ form }}` will render the form exactly as it is generated
        ```
        <input type="hidden" name="csrfmiddlewaretoken" value="fUVp4WL7fxTg83tYIqVhoQ7j4BuooMdACwbMABNr5qdGMJDAwq8zD2tvfuxji59m">
        

        <label for="id_name">Name:</label>
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <input type="text" name="name" maxlength="250" required="" id="id_name">


        <label for="id_image">Image:</label>
        Currently: <a href="/media/pics/bee.jpg">pics/bee.jpg</a><br>
        Change:
        <input type="file" name="image" accept="image/*" id="id_image">


        <label for="id_desc">Desc:</label>
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <textarea name="desc" cols="40" rows="10" required="" id="id_desc"></textarea>


        <label for="id_year">Year:</label>
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <input type="number" name="year" required="" id="id_year">
        ```
    - `{{ form.as_p }}` will render the form as a paragraph in the template, wrapped in `<p>` tags
        ```
        <input type="hidden" name="csrfmiddlewaretoken" value="XzKaOa7kPf6tzDNdAqzuy5ruKcBqCYVYkb0xkP9EF8qTdjXPoqMMNhNGV5ElwhRK">
        
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_name">Name:</label>
            <input type="text" name="name" maxlength="250" required="" id="id_name">
        </p>


        <p>
            <label for="id_image">Image:</label>
            Currently: <a href="/media/pics/bee.jpg">pics/bee.jpg</a><br>
            Change:
            <input type="file" name="image" accept="image/*" id="id_image">
        </p>


        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_desc">Desc:</label>
            <textarea name="desc" cols="40" rows="10" required="" id="id_desc"></textarea>
        </p>


        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_year">Year:</label>
            <input type="number" name="year" required="" id="id_year">
        </p>
        ```
    - `{{ form.as_table }}` will render the form as table cells wrapped in `<tr>` tags
    - `{{ form.as_ul }}` will render the form wrapped in `<li>` tags

## Example Projects

The following are some sample projects created based on the above documentation.

| # | Name | Action |
|---|---|---|
| 1 | Views & Templates | [Go to code](https://github.com/jothomas1996/django-view-template) |
| 2 | URL's | [Go to code](https://github.com/jothomas1996/django-site-urls) |
| 3 | Passing values between pages | [Go to code](https://github.com/jothomas1996/django-pass-value-page) |
| 4 | Static Site | [Go to code](https://github.com/jothomas1996/django-static-site) |
| 5 | Models & Admin Page | [Go to code](https://github.com/jothomas1996/django-models) |
| 6 | Account Handling | [Go to code](https://github.com/jothomas1996/django-account-handling) |
| 7 | CRUD Operations | [Go to code](https://github.com/jothomas1996/django-crud.git) |
| 8 | Class Based Views | [Go to code](https://github.com/jothomas1996/django-class-based-views.git) |