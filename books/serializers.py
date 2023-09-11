from rest_framework import serializers
from .models import Author, Book, Borrower, Loan


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'user']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'name', 'user']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'borrower', 'book', 'due_date']
