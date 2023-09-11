from typing import Optional
from django.views import generic
from django.shortcuts import render
from .models import Book, Author, Borrower, Loan
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import generics
from .serializers import AuthorSerializer, BookSerializer, BorrowerSerializer, LoanSerializer
from django.http import JsonResponse, Http404
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
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
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

@api_view(['GET', 'POST'])
def book_list(request:Request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request:Request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Http404
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=204)
@api_view()
def book_list2(request):
    return Response('ok')
from .serializers import BookSerializer
@api_view(['GET', 'PUT', 'DELETE'])
def api_book_details(request:Request, pk):
    book=Book.objects.get(pk=pk)
    serializer=BookSerializer(book)
    return Response(serializer.data)
