# Django Basics

Django is a free and open-source, Python-based web framework that follows the model–template–views architectural pattern. It is maintained by the Django Software Foundation, an independent organization established in the US as a 501 non-profit.

Model-View-Template, sometimes also referred to as MTV(Model-Template-View) is a design pattern or design architecture that Django follows to develop web applications. It is slightly different from the commonly known MVC(Model-View-Controller) design pattern.

- the python package `virtualenvwrapper-win` can be used to create virtual environments for the project
- open command window in main folder and execute `mkvirtualenv [environment_name]`
- if the created virtual environment is not automatially opened use command `workon [environment_name]`

- install django using `pip install django`
- to get any specific version use `pip install django==[version]`

- to create a project inside the main environment folder run the command `django-admin startproject [project_name]`
- adding a `.` at the end will tell django to use the current directory as the project folder

An app is a web application that does something – e.g., a blog system, a database of public records or a small poll app. A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.

- to run the created application in django server use command `python manage.py runserver`
- once this command is executed, check if the command line shows that there are any unapplied migrations
- if there are, then stop the server and execute `python manage.py migrate`
- the expected message when server is started is `System check identified no issues`

<hr>

- to create an app use code `python manage.py startapp [app_name]`
- add the app name `[app_name]` in the `INSTALLED_APPS` list in `settings.py` file of project

<hr>

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

<hr>

The next component that comes is a template. A template is basically an HTML file which is to be rendered by the view functions.

- templates are created and stored as normal html files by creating a folder named `templates` inside the corresponding app folder
- django can auto detect these files as the name `templates` is a part of the file structure
- if the templates are being created in any other location, the path must be added to `DIRS` list in the `TEMPLATES` list in `settings.py` file in main project folder
- to provide path, import the os package in `settings.py` and impliment `[os.path.join(BASE_DIR, 'folder_name_or_path')]`

- once the template files are created they can be rendered to the site using the render function

```
def hello_world(request):
	return render(request, 'hello.html')
```