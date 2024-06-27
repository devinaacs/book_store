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

7. Practice CRUD models with python shell
```bash
    python3 manage.py shell
```
```bash
    >>> from book_outlet.models import Book
```
```bash
    // inserting data
    >>> harry_potter = Book(title="Harry Potter 1 - The Philospher's Stone", rating=5)
    >>> harry_potter.save()
    >>> lord_of_the_rings = Book(title="Lord of the Rings", rating=4)
    >>> lord_of_the_rings.save()
```
```bash
    // getting all entries
    >>> Book.objects.all()
    >>> Book.objects.all()[0].author
```
```bash
    // updating data
    >>> harry_potter = Book.objects.all()[0]
    >>> harry_potter.author = "J.K. Rowling"
    >>> harry_potter.is_bestselling = True
    >>> harry_potter.save()
    >>> harry_potter.is_bestselling 
    True
```
```bash
    // deleting data
    >>> harry_potter = Book.objects.all()[0]
    >>> harry_potter.delete()
    (1, {'book_outlet.Book': 1}) 
    // (how many items deleted, wwhich model those deletions were)
```

