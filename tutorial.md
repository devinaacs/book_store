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

3. Creating Django Model
📂 ./book_outlet/models.py
```bash
    from django.db import models

    # Create your models here.

    class Book(models.Model):
        title = models.CharField(max_length=100)
        rating = models.IntegerField() 
```