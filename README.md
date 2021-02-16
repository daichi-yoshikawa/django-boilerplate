# django-boilerplate
A boilerplate which will be a good starting point for...
* Django API server assuming Single Page Application; Eg. Frontend is built purely by Vue.js and Django focuses on Backend
* Multi-tenant application working with Postgresql and gunicorn
* Unit test with pytest, not with Django test

## Requisites
Python 3.8 or later

## Get started
### Setup python
#### 1. Setup virtualenv
Using Python virtualenv is strongly recommended. There're many tutorials to set it up so google it.
#### 2. Pip install in virtualenv
```
$ pip install --upgrade pip
$ pip install -r requirements.txt
```
#### 3. Edit .env file
```
$ cp dot.env.default .env.development
```
Note: If you create .env file for production or test, create .env.production or .env.test respectively.
.env file includes the following environmental variables.
Variable Name | Definition

| Variable Name | Definition | Example |
| ------------- | ---------- | ------- | 
| APP_NAME | Application name. Used description in email, for example. | 'My Web App' |
| APP_DOMAIN | URL of app | '`http://localhost:8000`' |
| TENANT_DOMAIN_LENGTH | Length of tenant domain which is an identifier of each tenant used internally. | 32 |
| TENANT_INVITATION_CODE_LENGTH | Length of secret code randomly generated which is used to invite user(s) to a tenant | 32 |
| TENANT_INVITATION_CODE_LIFETIME_MINS | If minutes of this value passed, invitation code expires. | 360 |
| TENANT_INVITATION_CODE_REQUEST_MAX_SIZE | This number of users can be invited at the same time. | 50 |
| DJANGO_DEBUG | The same as Django build-in DJANGO_DEBUG flag. | True |
| DJANGO_SECRET_KEY | Secret key used to identify running Django application. | some-random-letters-hard-to-guess |
| POSTGRES_HOST | IP address of server where docker container for postgres runs. | 'localhost' |
| POSTGRES_CONTAINER_NAME | Docker container name for postgres service. | postgres_server_dev |
| POSTGRES_DB | Used DB name of postgres. | postgres_db_dev |
| POSTGRES_HOST_PORT | Port used for postgres docker container. | 5432 |
| POSTGRES_USER | User name for postgres. | user_dev |
| POSTGRES_PASSWORD | Password of postgres. | secret_password_hard_to_guess |
| POSTGRES_MOUNTED_VOLUME | Relative path to directory mounted to postgres docker container. | ./data/postgres_dev |
| DJANGO_TEMPLATE_DIR | Path to directory containing index.html. Relative to parent directory of root directory of this boilerplate. | vue-root-dir/dist/ |
| DJANGO_STATIC_DIR | Path to directory containing static files(css, js files). Relative to parent directory of root directory of this boilerplate. | vue-root-dir/dist/static/ |
| ACCESS_TOKEN_LIFETIME_MINS | Access token expires in this minutes. | 30 |
| REFRESH_TOKEN_LIFETIME_DAYS | Access token expires in this days. | 30 |
| UPDATE_LAST_LOGIN | If true, last_login data in users table is recorded. | True |
| EMAIL_VERIFICATION_CODE_LENGTH | Length of code randomly generated, which is used to verify email. | 32 |
| EMAIL_VERIFICATION_CODE_LIFETIME_MINS | If this minutes passed, email verification code expires. | 30 |
| EMAIL_BACKEND | Backend to send email. | django.core.mail.backends.smtp.EmailBackend |
| EMAIL_HOST | URL of used email server. | smtp.gmail.com (If use gmail.) |
| EMAIL_HOST_USER | Email address of sender. | `sender.my.awesome.app@xyz.xyz` |
| EMAIL_HOST_PASSWORD | Password of used email address. | secret-password-hard-to-guess |
| EMAIL_PORT | Port used by email server. | 587 |
| EMAIL_USE_TLS | Flag to indicate use of TLS. | True |
| MEDIA_ROOT | Directory name used to store media data(files). | media |
| MEDIA_URL | Relative path starting with '/' and ending with '/' to directory to store media data. | /media/ |
| PASSWORD_RESET_CODE_LENGTH | Length of code randomly generated, which is used to reset user password. | 32 |
| PASSWORD_RESET_CODE_LIFETIME_MINS | Password reset code expires if this minutes passed. | 30 |


#### 4. Launch docker container of postgres
To launch postgres server for development,
```
$ docker-compose --env-file .env.development up -d postgres
```
To launch postgres server for test,
```
$ docker-compose --env-file .env.test up -d postgres_test
```

#### 4.5 (Optional) Login postgres docker container
Install postgres client and login.
```
$ sudo apt install postgresql-client
$ psql -U <POSTGRES_USER> -h <POSTGRES_HOST> -p <POSTGRES_PORT> -d <POSTGRES_DB>
(You will be asked to enter password, so input <POSTGRES_PASSWORD>.)
Eg.
$ psql -U user_dev -h 127.0.0.1 -p 5432 -d postgres_dev
```

#### 5. Make migrations and migrate
To migrate for development,
```
$ cd <root-of-django-boilerplate>
$ DJANGO_ENV=development python manage.py makemigrations
$ DJANGO_ENV=development python manage.py migrate
```
To migrate for test,
```
$ cd <root-of-django-boilerplate>
$ DJANGO_ENV=development python manage.py makemigrations
$ DJANGO_ENV=development python manage.py migrate
```
If you mess up database tables for some reasons and would like to reset db, you can drop all tables by follow.
```
$ DJANGO_ENV=development python manage.py reset_db
OR
$ DJANGO_ENV=test python manage.py reset_db
```
#### 6. Run pytest to check if unit tests all passe
```
$ pytest
```
#### 7. Run development server
```
$ DJANGO_ENV=development python manage.py runserver
```


## Structure
### core
You define/extend models under this directory. Also, migration files are supposed to be contained in this.
If you implement commands used like "python manage.py \<command\>", core/management/commands is used. core/views has only one view by default. It is supposed to return index.html, which is a root html file used for a single page application.

### api
You define APIs under api/resources/v1. Serializers are stored in api/serializers. Unit tests for APIs are all implemented under api/tests directory.

### config
This directory is corresponding to a project directory generated by django-admin createproject command, that is, it contains settings.py, urls.py, and wsgi.py, etc.

### log
By default, log file is generated under this directory with name of application.log. You can change file name and log file location in settings.py, LOGGING value.

### static
For production, gunicorn or equivalent software is used instead of django development server. When using these software, you need to execute the follow first. Collected static files are stored in this directory.
```
$ DJANGO_ENV=production python manage.py collectstatic
```

### media
Files uploaded by users will be stored in this directory. For example, user image file is uploaded to media/images/user/]\<user-id\>/\<image-file\>.

### data
If you decide to launch postgres server on the same server where django is running, or for development, this directory may be used to be mounted to postgres docker container.

## Develop your web app
### Add more models
1. Create model file under core/models.
2. Define model class with base_models.BaseTenantModel for models which has tenant_id as foreign key or base_models.BaseModel for others.
3. Add the created class to core/models/\_\_init\_\_.py
4. Make migratiosn and migrate(See below). If you'd like to apply the migration to multiple envs, migrate for each env.
```
$ DJANGO_ENV=develpoment python manage.py makemigrations
$ DJANGO_ENV=development python manage.py migrate
$ DJANGO_ENV=test python manage.py migrate
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
