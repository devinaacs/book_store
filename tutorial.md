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
it will create file ./book_outlet/migrations/0001_initial.py

6. Updating Models & Migrations

📂 ./book_outlet/models.py
```bash
   from django.db import models
    from django.core.validators import MinValueValidator, MaxValueValidator

    # Create your models here.


    class Book(models.Model):
        title = models.CharField(max_length=100)
        rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
        author = models.CharField(null=True, max_length=100)
        is_bestselling = models.BooleanField(default=False)

        def __str__(self):
            return f"{self.title} ({self.rating})"

```
```bash
    python3 manage.py makemigrations
    python3 manage.py migrate 
```
it will create file ./book_outlet/migrations/0002_book_author_book_is_bestselling_alter_book_rating.py
