# blog_api :

## this a blog API built using Python, Django and Django REST framework

### To use it :
1. Make sure you are using python 2.7

1. Download (clone) the project to your chosen directory

1. Go to that direcotory :
`$ cd ....`

1. Create a new python virtual environment :
`$ virtualenv .`

1. Activate the virtual environment :
`$ source bin/activate`

1. Intsall the dependencies given in the requirements.txt file :
`$ pip install -r requirements.txt`

1. Then launch the server locally :

        $ cd src

        $ python manage.py makemigrations

        $ python manage.py migrate

        $ python manage.py createsuperuser  (if you want to create a superuser)

        $ python manage.py runserver

1. To quit the virtual environment :
`$ deactivate`


## Note that the app is still under development
