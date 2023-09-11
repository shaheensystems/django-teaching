from django.urls import path
from . import views
urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('borrower/<int:pk>/', views.BorrowerDetailView.as_view(), name='borrower_detail'),
    path('authors/active', views.AuthorsWithBooksView.as_view(), name='authors_with_books'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('unused_books/', views.UnusedBooksView.as_view(), name='unused_books'),
    path('borrowers/', views.BorrowerListView.as_view(), name='borrower_list'),
    path('popular_authors/', views.PopularAuthorsView.as_view(), name='popular_authors'),
    path('diverse_borrower/', views.MultiAuthorBorrowersView.as_view(), name='diverse_borrower'),
    #API URLS
    path('api/authors/', views.AuthorList.as_view(), name='author-list'),
    path('api/authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
    path('api/books/', views.book_list, name='book-list'),
    path('api/books/<int:pk>/', views.api_book_details, name='book-detail'),
]