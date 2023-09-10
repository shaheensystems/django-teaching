from typing import Optional
from django.views import generic
from django.shortcuts import render
from .models import Book, Author, Borrower, Loan
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'books/author_list.html'

class BorrowerDetailView(LoginRequiredMixin,UserPassesTestMixin, generic.DetailView):
    login_url = '/signin/'
    model = Borrower
    template_name = 'books/borrower_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_count'] = Loan.objects.filter(borrower=self.object).count()
        context['loaned_books'] = Loan.objects.filter(borrower=self.object)
        return context
    def test_func(self) :
        #get borrower with requested id
        borrower = self.get_object()
        #return if it is same as logged in user
        return self.request.user == borrower.user
class AuthorsWithBooksView(generic.ListView):
    model = Author
    template_name = 'books/authors_with_books.html'

    def get_queryset(self):
        return Author.objects.annotate(book_count=Count('book')).filter(book_count__gte=1)
# ... Existing imports and views ...

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'books/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=self.object)
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loans'] = Loan.objects.filter(book=self.object)
        return context

class UnusedBooksView(generic.ListView):
    model = Book
    template_name = 'books/unused_books.html'

    def get_queryset(self):
        return Book.objects.annotate(loan_count=Count('loan')).filter(loan_count=0)
class BorrowerListView(generic.ListView):
    model = Borrower
    template_name = 'book/borrower_list.html'
    
    def get_queryset(self):
        return Borrower.objects.annotate(num_loans=Count('loan'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowers = context['object_list']
        for borrower in borrowers:
            borrower.loans = Loan.objects.filter(borrower=borrower)
        return context

class PopularAuthorsView(generic.ListView):
    model = Author
    template_name = 'books/popular_authors.html'

    def get_queryset(self):
        return Author.objects.annotate(num_books=Count('book')).filter(num_books__gt=2)
class MultiAuthorBorrowersView(generic.ListView):
    model = Borrower
    template_name = 'books/diverse_borrower.html'

    def get_queryset(self):
        return Borrower.objects.annotate(
            num_authors=Count('loan__book__author', distinct=True)
        ).filter(num_authors__gt=1)