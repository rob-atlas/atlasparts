from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime

from .forms import ProductForm
from .models import Product


# Create your views here.
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()

    context = {
        'form': form,
        'title': "New Part",
        'year':datetime.now().year,
    }
    return render(request, "catalog/product_create.html", context)


def index(request):
    context = {
        'title':'Atlas Parts',
        'year':datetime.now().year,
    }
    return render(request, 'catalog/index.html', context)


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    context = {
        'title':'Contact',
        'message':'Atlas Gaming contact information.',
        'year':datetime.now().year,
    }
    return render( request, 'catalog/contact.html', context )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    context = {
        'title':'About this app',
        'message':'This application is about the tracking of parts inside the Production department of Atlas Gaming.',
        'year':datetime.now().year,
    }
    return render( request, 'catalog/about.html', context )
