# django-boilerplate
A boilerplate which will be a good starting point for...
* Django RESTful API server for Single Page Application
* Multi-tenant application working with Postgresql and gunicorn
* Unit test with pytest, not with Django test
* Authorization by JWT access/refresh tokens

## Requisites
* Python 3.8 or later
* django 3.1 or later
* django_rest_framework, django_rest_framework_simplejwt
* django-environ, django-cleanup
* psycopg2-binary
* pytest, pytest-django, pytest-env, pytest-order
* Docker, docker-compose

You can see the details of used python packages in requirements.txt.
Major packages are illustrated in the table below.
#### Table of installed python packages
| Package | Usage |
| ------- | ------ |
| djangorestframework | Implement RESTful API classes |
| djangorestframework-simplejwt | Json web token used for auth |
| django-environ | Read .env file |
| django-cleanup | Uploaded file in dir is properly deleted |
| gunicorn | Python wsgi http server used for production |
| psycopg2-binary | Access to postgresql DB |
| pytest | Unit test tool alternative to built-in Django test |
| pytest-django | pytest extention for django framework |
| pytest-env | Enable to set env vars  in pytest.ini |
| python-box | Enable dot access of dictionary values |

## Get started
### 0. Use docker-compose
If you use docker-compose, you just follow step 3, 7 and 9 first. And then launch docker-compose as below.
```
$ docker-compose up -d
```
You can check containers are running correctly.
```
$ docker ps -a
```
Once you checked containers are up and running, proceed to step 11.

### 1. Setup python virtualenv
Using Python virtualenv is strongly recommended. There're many tutorials to set it up so google it.
### 2. Pip install in virtualenv
```
$ pip install --upgrade pip
$ pip install -r requirements.txt
```
### 3. Edit .env file (or pytest.ini for test)
Environmental variables for development and production are supposed to be set in .env file located in root directory, and ones for test are defined in pytest.ini file. If you work on .env, you can use dot.env.default, which is a template of .env.
```
$ cp dot.env.default .env
```
#### Table of Environmental Variables
| Variable Name | Definition | Example |
| ------------- | ---------- | ------- | 
| <sup><b>APP_NAME</b></sup> | Application name. Used description in email, for example. | 'My Web App' |
| <sup><b>APP_DOMAIN</b></sup> | URL of app | '`http://localhost:8000`' |
| <sup><b>TENANT_DOMAIN_LENGTH</b></sup> | Length of tenant domain which is an identifier of each tenant used internally. | 32 |
| <sup><b>TENANT_INVITATION_CODE_LENGTH</b></sup> | Length of secret code randomly generated which is used to invite user(s) to a tenant | 32 |
| <sup><b>TENANT_INVITATION_CODE_LIFETIME_MINS</b></sup> | If minutes of this value passed, invitation code expires. | 360 |
| <sup><b>TENANT_INVITATION_CODE_REQUEST_MAX_SIZE</b></sup> | This number of users can be invited at the same time. | 50 |
| <sup><b>DJANGO_DEBUG</b></sup> | The same as Django build-in DJANGO_DEBUG flag. | True |
| <sup><b>DJANGO_SECRET_KEY</b></sup> | Secret key used to identify running Django application. | some-random-letters-hard-to-guess |
| <sup><b>POSTGRES_HOST</b></sup> | IP address of server where docker container for postgres runs. | 'localhost' |
| <sup><b>POSTGRES_CONTAINER_NAME</b></sup> | Docker container name for postgres service. | postgres_server_dev |
| <sup><b>POSTGRES_DB</b></sup> | Used DB name of postgres. | postgres_db_dev |
| <sup><b>POSTGRES_HOST_PORT</b></sup> | Port used for postgres docker container. | 5432 |
| <sup><b>POSTGRES_USER</b></sup> | User name for postgres. | user_dev |
| <sup><b>POSTGRES_PASSWORD</b></sup> | Password of postgres. | secret_password_hard_to_guess |
| <sup><b>POSTGRES_MOUNTED_VOLUME</b></sup> | Relative path to directory mounted to postgres docker container. | ./data/postgres_dev |
| <sup><b>DJANGO_TEMPLATE_DIR</b></sup> | Path to directory containing index.html. Relative to parent directory of root directory of this boilerplate. | vue-root-dir/dist/ |
| <sup><b>DJANGO_STATIC_DIR</b></sup> | Path to directory containing static files(css, js files). Relative to parent directory of root directory of this boilerplate. | vue-root-dir/dist/static/ |
| <sup><b>ACCESS_TOKEN_LIFETIME_MINS</b></sup> | Access token expires in this minutes. | 30 |
| <sup><b>REFRESH_TOKEN_LIFETIME_DAYS</b></sup> | Access token expires in this days. | 30 |
| <sup><b>UPDATE_LAST_LOGIN</b></sup> | If true, last_login data in users table is recorded. | True |
| <sup><b>EMAIL_VERIFICATION_CODE_LENGTH</b></sup> | Length of code randomly generated, which is used to verify email. | 32 |
| <sup><b>EMAIL_VERIFICATION_CODE_LIFETIME_MINS</b></sup> | If this minutes passed, email verification code expires. | 30 |
| <sup><b>EMAIL_BACKEND</b></sup> | Backend to send email. | django.core.mail.backends.smtp.EmailBackend |
| <sup><b>EMAIL_HOST</b></sup> | URL of used email server. | smtp.gmail.com (If use gmail.) |
| <sup><b>EMAIL_HOST_USER</b></sup> | Email address of sender. | `sender.my.awesome.app@xyz.xyz` |
| <sup><b>EMAIL_HOST_PASSWORD</b></sup> | Password of used email address. | secret-password-hard-to-guess |
| <sup><b>EMAIL_PORT</b></sup> | Port used by email server. | 587 |
| <sup><b>EMAIL_USE_TLS</b></sup> | Flag to indicate use of TLS. | True |
| <sup><b>MEDIA_ROOT</b></sup> | Directory name used to store media data(files). | media |
| <sup><b>MEDIA_URL</b></sup> | Relative path starting with '/' and ending with '/' to directory to store media data. | /media/ |
| <sup><b>PASSWORD_RESET_CODE_LENGTH</b></sup> | Length of code randomly generated, which is used to reset user password. | 32 |
| <sup><b>PASSWORD_RESET_CODE_LIFETIME_MINS</b></sup> | Password reset code expires if this minutes passed. | 30 |


### 4. Launch docker container of postgres
To launch postgres server for development,
```
$ docker-compose up -d postgres
```
To launch postgres server for test,
```
$ docker-compose -f docker-compose.test.yml up -d postgres
```

### 4.5 (Optional) Login postgres docker container
Install postgres client and login.
```
$ sudo apt install postgresql-client
$ psql -U <POSTGRES_USER> -h <POSTGRES_HOST> -p <POSTGRES_PORT> -d <POSTGRES_DB>
(You will be asked to enter password, so input <POSTGRES_PASSWORD>.)
Eg.
$ psql -U user_dev -h 127.0.0.1 -p 5432 -d postgres_dev
```

### 5. Make migrations and migrate
To migrate for development,
```
$ cd <root-of-django-boilerplate>
$ python manage.py makemigrations
$ python manage.py migrate
```
If you mess up database tables for some reasons and would like to reset db, you can drop all tables by follow. You don't need to call the follow for test because reset\_db and migrate are called every time pytest is executed.
```
$ python manage.py reset_db
```
For test, you don't need to call migrate because the commands to reset and migrate db tables used for test are internally called as you can see in api/tests/conftest.py.
```
$ cd <root-of-django-boilerplate>
$ python manage.py makemigrations
```
### 6. Run pytest to check if unit tests all pass
```
$ pytest
```
If you'd like to add options, edit pytest.ini file.

### 7. Prepare index.html
Prepare index.html which is used for your single page application. You can use [vue-boilerplate](https://github.com/daichi-yoshikawa/vue-boilerplate).

In case of using vue-boilerplate, you can place it at the same level as django-boilerplate as below.
```
Web application root
├── vue-boilerplate (Of course you will have different name for your project)
└── django-boilerplate (Of course you will have different name for your project)
```

By default, vue-boilerplate will generate index.html under vue-boilerplate/dist/ and bundled js and css files under vue-boilerplate/dist/static directories respectively.
For more details, refer to README.md of vue-boilerplate.

### 8. Run development server (production? Proceed to section 9-10)
```
$ python manage.py runserver
```

### 9. Edit gunicorn config file (for production)
Edit gunicorn.conf.py to configure gunicorn. This file is automatically loaded when gunicorn is launched. If you use development server, you don't need to edit this file.

### 10. Run gunicorn (for production)
In order to run gunicorn, execute the following command,
Or you can use docker-compose.yml as illustrated in step 1.
```
$ gunicorn config.wsgi
```
If you use development server provided by django, you don't need to run gunicorn.

### 11. Access to index.html
Open your favorite browser, and input localhost:8000/entry. You'll see entry page of sample web app now :)

## Directory Structure
### core
You define/extend models under this directory. Also, migration files are supposed to be contained in this.
If you implement commands used like "python manage.py \<command\>", core/management/commands is used. core/views has only one view by default. It is supposed to return index.html, which is a root html file used for a single page application.

### api
You define APIs under api/resources/v1. Serializers are stored in api/serializers. Unit tests for APIs are all implemented under api/tests directory.
You may think why models are "core" directory rather than "api". It's because models may be referred broadly. For example, they may be used to implement 
custom commands which are stored/implemented core/management/commands directory. 

### config
This directory is corresponding to a project directory generated by django-admin createproject command, that is, it contains settings.py, urls.py, and wsgi.py, etc.

### log
By default, log file is generated under this directory with name of application.log. You can change file name and log file location in settings.py, LOGGING value.

### static
For production, gunicorn or equivalent software is used instead of django development server. When using these software, you need to execute the follow first. Collected static files are stored in this directory.
```
$ python manage.py collectstatic
```

### media
Files uploaded by users will be stored in this directory. For example, user image file is uploaded to media/images/user/]\<user-id\>/\<image-file\>.

### data
If you decide to launch postgres server on the same server where django is running, or for development, this directory may be used to be mounted to postgres docker container.

### core/management/commands
Custom commands which can be called in format of "python manage.py \<your-custom-command\>" are supposed to be stored here.

## Develop your web app
### Add more models
1. Create model file under core/models.
2. Define model class with base_models.BaseTenantModel for models which has tenant_id as foreign key or base_models.BaseModel for others.
3. Add the created class to core/models/\_\_init\_\_.py
4. Make migratiosn and migrate(See below). If you'd like to apply the migration to multiple envs, migrate for each env.
```
$ python manage.py makemigrations
$ python manage.py migrate
```

### Add serializers
1. Create serializer file under api/serializers.
2. Define serializer class with BaseModelSerializer. If needed, overwrite create, update, or validate methods. When you ovewrite create or update, <b>do not forget to call "validated_data = self.createrstamp(validated_data)" and "validated_data = self.updaterstamp(validated_data)" respectively.</b>
3. Add created serializer to api/serializers/\_\_init\_\_.py.

### Add new APIs
1. Create api file under api/resources/v1 directory. File name is singular and corresponds to model file name if possible.
2. Implement APIs using rest_framework package. By default views are implemented as derived class of rest_framework.views.APIView. Use api.resources.decorators.tenant_api if the endpoint is tenantwise, and use api.resources.decorators.tenant_user_api if the endpoint is tenant_user wise. If tenant_api decorator is used, the first 3 arguments are self, request, tenant respectively. And if tenant_user_api decorator is used, the first 3 arguments are self, request, tenant_user respectively.
3. Add created API view class to api/resources/v1/\_\_init\_\_.py.
4. Add endpoint for the created API view class to api/urls/v1.py.

### Add unit test
Add unit tests for APIs should be under api/tests/v1. Other than that, for example helper functions, are stored in api/tests/helpers.

### Add constant values, or helper functions used broadly
These are all implemented in constants.py, or utils.py files under api/common directory.
When you define constant value, define class inheriting Enum to make it uneditable.

### Add custom exceptions
Exceptions are implemented in api/common/exceptions.py file. Inherit rest_framework.exceptions.APIException.
If you'd like to assign specific HTTP status code for each exception, edit api/resources/exception_handler.py, exc2status_map dictionary.

## Default endpoints
| Endpoint | Usage | Request | Auth Required |
| -------- | ----- | --------| ------------- |
| <sup><b>POST /api/v1/token/</b></sup> | Get access token and refresh token | email, password | False |
| <sup><b>POST /api/v1/token/refresh/</b></sup> | Refresh access token | refresh | True |
| <sup><b>POST /api/v1/token/verify/</b></sup> | Verify access token validity | N/A | True |
| <sup><b>POST /api/v1/token/revoke/</b></sup> | Revoke access token and refresh token | refresh | True |
| <sup><b>POST /api/v1/users/</b></sup> | Create user account | first_name, last_name, email, image, password, verification_code or invitation_code | True |
| <sup><b>GET /api/v1/users/\<int:id\>/</b></sup> | Get user data | N/A | True |
| <sup><b>PUT /api/v1/users/\<int:id\>/</b></sup> | Update user data | first_name and\/or last_name and\/or image | True |
| <sup><b>DELETE /api/v1/users/\<int:id\>/</b></sup> | Delete user account | N/A | True |
| <sup><b>PUT /api/v1/users/\<int:id\>/password/</b></sup> | Update user password | password, new_password | True |
| <sup><b>GET /api/v1/users/\<int:id\>/tenants/</b></sup> | Get associated tenant list | N/A | True |
| <sup><b>POST /api/v1/email/signup/verification/</b></sup> | Create email verification code and send signup link by email | email | False |
| <sup><b>POST /api/v1/password/reset-code/</b></sup> | Create password reset code and send reset link by email | email | False |
| <sup><b>POST /api/v1/password/reset/</b></sup> | Reset password with reset code | email, reset_code | False |
| <sup><b>POST /api/v1/tenants/</b></sup> | Create tenant | name, description | True |
| <sup><b>GET /api/v1/tenants/\<str:domain\>/</b></sup> | Get tenant data | N/A | True |
| <sup><b>POST /api/v1/tenants/\<str:domain\>/invitation_codes/</b></sup> | Create invitation code to tenant and send link by email | tenant_id, tenant_user_id, email | True |
| <sup><b>POST /api/v1/tenants/invited/</b></sup> | Get invited tenant data | email, invitation_code | True |
| <sup><b>GET /api/v1/tenants/\<str:domain\>/users/</b></sup> | Get tenant user list of tenant with specified domain | N/A | True |
| <sup><b>POST /api/v1/tenants/\<str:domain\>/users/</b></sup> | Create tenant user | tenant_id, user_id, invitation_code | True |
| <sup><b>GET /api/v1/tenants/\<str:domain\>/users/\<int:id\>/</b></sup> | Get tenant user data | N/A | True |

## Helpful Commnads for Trouble Shooting
### Clearning up docker containers
Check existing containers.
```
$ docker container ls -a
```
Stop and remove all containers.
```
$ docker stop $(docker ps -q)
$ docker rm $(docker ps -qa)
```
Delete all images
```
$ docker rmi $(docker images -q)
```
Get in terminal in running container.
```
$ docker exec -it <container name/ID> /bin/bash
```

### Clearning up database
You may need to delete directory mounted to postgres docker container, especially when you clean up all relevant docker containers to start over the setup.
```
Eg.)
$ sudo rm -r ./data/postgres_dev
```
Or you may like to clear all record in db and reset sequences as well. In the case drop all tables and rebuild tables again.
```
$ python manage.py reset_db
$ python manage.py migrate
```


