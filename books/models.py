from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author.name}"
    def get_absolute_url(self):
        return reverse('book_details', kwargs={'pk': self.pk})
class Borrower(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='borrower')

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Loan(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    due_date = models.DateField()

    def __str__(self):
        return f"Loan of '{self.book.title}' to {self.borrower.name} due on {self.due_date}"
class Admin(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Review of '{self.book.title}' by {self.borrower.name} ({self.rating} stars"
class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f"{self.name}"