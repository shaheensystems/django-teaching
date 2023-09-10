from django.utils.html import format_html
from django.contrib import admin
from .models import Author, Book, Borrower, Loan

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  
    search_fields = ('name', 'user__username')  
    list_filter = ('name',)  

class BookAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if(obj.cover_image):
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.cover_image.url))
        else:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(''))
    def existing_cover_image(self, obj):
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.cover_image.url,
            width='50%',
            height="auto",
            )
        )
    list_display = ('title', 'author', 'image_tag')  
    search_fields = ('title', 'author__name')  
    list_filter = ('title','author__name',)  
    readonly_fields = ("existing_cover_image",)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  
    search_fields = ('name', 'user__username')  

class LoanAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'book', 'due_date')  
    search_fields = ('borrower__name', 'book__title')  
    list_filter = ('due_date',)  

# Registering the models and their respective admin classes
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Loan, LoanAdmin)