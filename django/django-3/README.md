## Install dependencies 
Change directory to root project directory 

```bash
pip install -r requirements.txt 

``` 

## Apply migrations 
```bash
python manage.py makemigrations news
python manage.py migrate 

```

## Run the project 
```bash
python manage.py runserver 

```

The project will be available at: localhost:8000 

## Run the tests 
```bash 
python manage.py test news 

```




