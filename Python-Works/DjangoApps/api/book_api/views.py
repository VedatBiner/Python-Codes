from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from book_api.models import Book
from book_api.serializer import BookSerializer

# requesti filtrelemek için decorator kullanalım.
# Bütün kayıtları okuyoruz
@api_view(['GET', 'POST'])
def books(request):

    # request GET mi?
    if request.method == "GET":
        books = Book.objects.all()
        # Dönüşümün yapılması
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    # request POST mu ?
    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        # validation işlemi
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

# Burada GET request ile tek bir kayıt okuyoruz
@api_view(['GET', 'PUT', 'DELETE'])
def book(request, id):

    try:
        # veriyi oku
        book = Book.objects.get(pk=id)
    except:
        return Response(
            {"error":"Eşleşen bir kayıt bulunamadı !!!"}, 
            status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        # güncelenecek bilgiyi ver
        serializer = BookSerializer(book, data=request.data)
        # validasyon
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "DELETE":
        # veriyi sil
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
