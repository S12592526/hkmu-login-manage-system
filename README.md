# hkmu-login-manage-system



## Project Structure：

admin：WEB Directory

project：Server Directory



------



### Server Description：

#### 1、System Requirements

Python 3.8

Django 4.2.7

Redis 5.0.14+

MySQL 8.0.32

#### 2、Install

（1）Install using `pip`： `pip install -Ur requirements.txt`

（2）Creating a database `student_management_system ` , character set `utf8mb4` , collation `utf8mb4_general_ci` 

（3）Database Import `student_management_system_new.sql`

#### 3、Preparation Before Operation

modify `project/setting.py` , Modify the database configuration as follows：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'student_management_system',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '12345678',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        },
        'MYSQL': {
            'driver': 'pymysql',
            'charset': 'utf8mb4'
        }
    }
}

```

#### 4、Startup Project

execute： `python manage.py runserver`

The project will use `8000` ports



------



### WEB Description：

#### 1、System Requirements

Node.js 18.18.0

Npm 10.1.0

#### 2、Install

execute： `npm install`

#### 3、Startup Project

execute： `npm run dev`

After successful startup, the login page will automatically open.