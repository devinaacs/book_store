1. Setting Up the Starting Project
```bash
    django-admin startproject my_site
```
<br>

2. Create New App
```bash
    python3 manage.py startapp book_outlet
```
<br>

3. Add Book Outlet App definition on settings.py 
```bash
    INSTALLED_APPS = [
        ...,
        'book_outlet',
    ]
```
<br>

4. Creating Django Model

📂 ./book_outlet/models.py
```bash
    from django.db import models

    # Create your models here.

    class Book(models.Model):
        title = models.CharField(max_length=100)
        rating = models.IntegerField() 
```

5. Make Migrations
```bash
    python3 manage.py makemigrations
    python3 manage.py migrate 
```
