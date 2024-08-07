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
    <QuerySet [<Book: Harry Potter 1 - The Philospher's Stone (5)>, <Book: Lord of the Rings (4)>]>
    >>> Book.objects.all()[0].author    
```
```bash
    // updating data
    >>> harry_potter = Book.objects.all()[0]
    >>> harry_potter.author = "J.K. Rowling"
    >>> harry_potter.is_bestselling = True
    >>> harry_potter.save() 
    >>> Book.objects.all()[0].author
    'J.K. Rowling'
```
```bash
    // deleting one data
    >>> harry_potter.delete()
    (1, {'book_outlet.Book': 1})
    // (how many items deleted, wwhich model those deletions were)
    >>> Book.objects.all()
    <QuerySet [<Book: Lord of the Rings (4)>]>

    // delete all data
    >>> Book.objects.all().delete()
    (2, {'book_outlet.Book': 2})
```
```bash
    // create instead save
    >>> Book.objects.create(title="Harry Potter 1", rating=5, author="J.K. Rowling", is_bestselling=True)
    <Book: Harry Potter 1 (5)>
    >>> Book.objects.all()
    <QuerySet [<Book: Lord of the Rings (4)>, <Book: Harry Potter 1 (5)>]>
```
```bash
    // querying & filtering data
    
    // get only will return one data (unique key), or it would be error
    >>> Book.objects.get(id=2)      
    <Book: Lord of the Rings (4)>
    >>> Book.objects.get(title="Harry Potter 1")
    <Book: Harry Potter 1 (5)>

    // filter
    >>> Book.objects.filter(is_bestselling=True)
    <QuerySet [<Book: Lord of the Rings (4)>, <Book: Harry Potter 1 (5)>]>
    >>> Book.objects.filter(rating__gte=4)
    <QuerySet [<Book: Lord of the Rings (4)>, <Book: Harry Potter 1 (5)>]>
    >>> Book.objects.filter(rating__gte=4, title__icontains="harry")
    <QuerySet [<Book: Harry Potter 1 (5)>]>
```
reference: https://docs.djangoproject.com/en/5.0/ref/models/querysets/
```bash
    // filter with "or" conditions
    >>> from django.db.models import Q
    >>> Book.objects.filter(Q(rating__gte=4) | Q(is_bestselling=False))
    <QuerySet [<Book: Lord of the Rings (4)>, <Book: Harry Potter 1 (5)>]>

    // filter both "or" and "and"
    >>> Book.objects.filter(Q(rating__gte=4) | Q(is_bestselling=False), Q(author="J.K. Rowling"))
    <QuerySet [<Book: Harry Potter 1 (5)>]>
```
```bash
    // Query performance
    >>> bestsellers = Book.objects.filter(is_bestselling=True) // it also cached the result
    >>> amazing_bestsellers = bestsellers.filter(rating__gt=4)
    >>> print(bestsellers)
    <QuerySet [<Book: Lord of the Rings (4)>, <Book: Harry Potter 1 (5)>]>
    >>> print(amazing_bestsellers)
    <QuerySet [<Book: Harry Potter 1 (5)>]>
```

7. Model URLs
📂 ./book_outlet/models.py
```bash
    ...
    from django.urls import reverse

    class Book(models.Model):
        ...
        def get_absolute_url(self):
            return reverse("book-detail", args=[self.id])
```
📂 ./book_outlet/templates/book_outlet/index.html
```bash
    // using id
        <a href="{% url 'book-detail' book.id %}">
            <li>{{ book.title }} (Rating: {{ book.rating }})</li>
        </a> 
    // using model get_absolute_url
        <a href="{{ book.get_absolute_url }}">
            <li>{{ book.title }} (Rating: {{ book.rating }})</li>
        </a>
            
```

8. Adding a Slugfield & Overwritting Save
📂 ./book_outlet/models.py
```bash
    ...
    from django.urls import reverse
    from django.utils.text import slugify

    class Book(models.Model):
        ....
        slug = models.SlugField(default="", null=False)

        def ... 
        
        def save(self, *args, **kwargs):
            self.slug = slugify(self.title)
            return super().save(*args, **kwargs)
```

```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py shell
```
```bash
    >>> Book.objects.get(title="Harry Potter 1").save()
    >>> Book.objects.get(title="Lord of the Rings").save()
    >>> Book.objects.get(title="Lord of the Rings").slug
    'lord-of-the-rings'
```

9. Aggregation & Ordering
📂 ./book_outlet/views.py
```bash
    ...
    from django.db.models import Avg
    # Create your views here.


    def index(request):
        books = Book.objects.all().order_by("title")
        num_books = books.count()
        avg_rating = books.aggregate(Avg("rating"))
        
        return render(request, "book_outlet/index.html", {
            "books": books,
            "totatl_number_of_books": num_books,
            "average_rating": avg_rating['rating__avg']
        })
```

10. Logging Data Into the Admin
```bash
    python3 manage.py createsuperuser
    Username (leave blank to use 'devinacecilia'): dev
    Email address: cecildevinaa@gmail.com
    Password: shinichikudo
    Password (again): shinichikudo 
    Superuser created successfully.
```

11. Working with relation in Python Code
```bash
    python3 manage.py shell   
    >>> from book_outlet.models import Book, Author
    >>> jkrowling = Author(first_name="J.K.", last_name="Rowling")
    >>> jkrowling.save()
    >>> hp1 = Book(title="Harry Potter and the Philosopher's Stone", rating=5, author=jkrowling, is_bestselling=True)
    >>> hp1.save()
    >>> Book.objects.all()[0]
    <Book: Harry Potter and the Philosopher's Stone (5)>
    >>> hp1.author.last_name
    'Rowling'
```

12. Cross Model Queries
```bash
    python3 manage.py shell   
    >>> from book_outlet.models import Book, Author
    >>> harrypotter = Book.objects.get(title="Harry Potter and the Philosopher's Stone")
    >>> books_by_rowling = Book.objects.filter(author__last_name="Rowling")
    >>> books_by_rowling
    <QuerySet [<Book: Harry Potter and the Philosopher's Stone (5)>]>

    >>> books_by_rowling = Book.objects.filter(author__last_name__contains="wling")
    >>> books_by_rowling
    <QuerySet [<Book: Harry Potter and the Philosopher's Stone (5)>]>

    >>> jkr = Author.objects.get(first_name="J.K.")
    >>> jkr
    <Author: Author object (1)>
    >>> jkr.book_set
    <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x106ad3ef0>
```

📂 ./book_outlet/models.py
```bash
    ...

    class Book(models.Model):
        ....
        author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
```
```bash
    python3 manage.py shell  
    >>> from book_outlet.models import Book, Author
    >>> jkr = Author.objects.get(first_name="J.K.")
    >>> jkr.books.all()
    <QuerySet [<Book: Harry Potter and the Philosopher's Stone (5)>]>
    >>> jkr.books.get(title="Harry Potter and the Philosopher's Stone")
    <Book: Harry Potter and the Philosopher's Stone (5)>
    >>> jkr.books.filter(rating__gt=3)
    <QuerySet [<Book: Harry Potter and the Philosopher's Stone (5)>]>
```

13. Managing Relations in Admin

📂 ./book_outlet/admin.py
```bash
    ...
    from .models import Book, Author

    ...
    admin.site.register(Author)
```

📂 ./book_outlet/models.py
```bash
    ...

    class Author(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        
        def full_name(self):
            return self.first_name + ' ' + self.last_name
        
        def __str__(self):
            return self.full_name()
    
    ...
```
14. Adding a one-to-one Relations

📂 ./book_outlet/models.py
```bash
    ...

    class Address(models.Model):
        street = models.CharField(max_length=80)
        postal_code = models.CharField(max_length=5)
        city = models.CharField(max_length=50)
        
    class Author(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True,)
        
        def full_name(self):
            return self.first_name + ' ' + self.last_name
        
        def __str__(self):
            return self.full_name()
    ...
```
```bash
    python3 manage.py shell   
    >>> address1 = Address(street="44-46 Morningside Road",postal_code="EH101",city="Edinburgh")
    >>> address2 = Address(street="267 Banbury Road",postal_code="OX27H",city="Oxford")
    >>> address1.save()
    >>> address2.save()
    >>> jkr = Author.objects.get(first_name="J.K.")
    >>> jkr.address = address1
    >>> jkr.save()
    >>> jrrt = Author.objects.get(last_name="Tolkien")
    >>> jrrt.address = address2
    >>> jrrt.address 
    <Address: Address object (2)>
```

15. One-to-one & Admin Config

📂 ./book_outlet/admin.py
```bash
    ...
    from .models import Book, Author, Address

    ...
    admin.site.register(Address)
```
📂 ./book_outlet/models.py
```bash
    class Address(models.Model):
        street = models.CharField(max_length=80)
        postal_code = models.CharField(max_length=5)
        city = models.CharField(max_length=50)

        def __str__(self):
            return f"{self.street}, {self.postal_code}, {self.city}"
        
        class Meta:
            verbose_name_plural = 'Address Entries'
```

16. Setting up many-to-many

📂 ./book_outlet/models.py
```bash
    class Country(models.Model):
        name = models.CharField(max_length=80)
        code = models.CharField(max_length=2) 
        
    class Book(models.Model):
        ...
        published_countries = models.ManyToManyField(Country)

```
```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
```


17. Using Many-To-Many in Python
```bash
    python3 manage.py shell
    >>> germany = Country(name="Germany", code="DE")
    >>> germany.save()
    >>> hp1= Book.objects.all()[0]
    >>> hp1.published_countries.add(germany)
    >>> hp1.published_countries.all()
    <QuerySet [<Country: Country object (1)>]>
```

18. Many-to-Many in Admin

📂 ./book_outlet/admin.py
```bash
    ...
    from .models import Book, Author, Address, Country

    ...
    admin.site.register(Country)
```
📂 ./book_outlet/models.py
```bash
    class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2) 
    
    class Meta: 
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name
```

