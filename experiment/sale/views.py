import os
import requests
from datetime import date

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .unleashed.auth import UnleashedAuth

# ROB: not sure if that is how it is done but I want to
#      look up the Unleashed product code and get the game name back
from catalog.models import UnleashedProductCode
from .models import UnleashedSalesOrder, UnleashedLineItem

all_ptms = {
    '26-273': 'IGT Nextgen with TFT',
    '26-275': 'Standard blank panel',
    '26-276': 'IGT Nextgen',
    '26-277': 'IGT iDisplay',
    '26-278': 'Aristocrat Prime',
    '26-279': 'Konami',
    '26-280': 'Aristocrat Dacom 5000',
    '26-281': 'Aristocrat Dacom 6000',
    '26-297': 'Bally with TFT',
    '26-298': 'Bally',
}

# Create your views here.
def index(request):
    if request.method == "POST":
        context = { 'data': 'Here is some info on the sales order' }
        template = 'sale/sale.html'
    else:
        info = get_unleashed_data()
        if isinstance(info, str):
            return HttpResponse(info)
        sales = extract_wanted_info(info)
        context = { 'orders': sales }
        template = 'sale/index.html'

    return render(request, template, context)


def get_unleashed_data():
    """
    load information from unleashed url
    Using the API id & key from environment variables
    We will get back a json file if successful
    or we return a text string with the error
    """
    data = None

    # Difference between Windows and Other OS
    if(os.supports_bytes_environ is True):
        api_id = os.environb.get(b'UNLEASHED_API_ID')
        api_key = os.environb.get(b'UNLEASHED_API_KEY')
    else:
        api_id = bytes(os.environ.get('UNLEASHED_API_ID'), 'latin-1')
        api_key = bytes(os.environ.get('UNLEASHED_API_KEY'), 'latin-1')

    api_url = os.environ.get('UNLEASHED_API_URL')

    if api_id is None:
        return "UNLEASHED_API ID has not been set\nUse 'export UNLEASHED_API_ID=1234'"
    if api_key is None:
        return "UNLEASHED_API_KEY has not been set\nUse 'export UNLEASHED_API_KEY=1234'"
    if api_url is None:
        return "UNLEASHED_API URL has not been set\nUse 'export UNLEASHED_API_URL=http://blahblah'"

    turl = api_url + "SalesOrders?orderStatus=Backordered,Parked"
    theaders = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }
    tparams = {}

    # ROB 'timeout' is important!
    #     It determines how long a requests waits for data
    #     otherwise it waits indefinitely
    tauth = UnleashedAuth(api_id, api_key)
    r = requests.get(turl, headers=theaders, params=tparams, auth=tauth,
                     timeout=10.0)

    if r.status_code == requests.codes.ok:
        data = r.json()
    else:
        data = "Unable to get information from unleashed\n" + \
               "Returned error code: " + str(r.status_code)
    """
    # Temporarily write the result to a file
    if r.status_code == requests.codes.ok :
        with open("SalesOrders.json", 'w') as fd:
            # json.dump(r.json()['Pagination'], fd)
            json.dump(r.json(), fd)
    """
    return data


def extract_wanted_info(data):
    """
    From the data supplied extract only the items we are interested

    Quantity is related to EGMs and games only, no other line items
    need to work out exactly what is needed to be displayed
    Examples:
        Sales Order: 1 EGM and 1 Game
        QTY = 1 (One EGM with one game)
        
        Sales Order: 1 EGM and 2 games
        QTY = 2 (one EGM and one Game Conversion)
        
        Sales Order: 1 EGM and 4 games
        QTY = 4 (one EGM and three Game Conversions)

        Sales Order: 3 EGM and 4 games
        QTY = 4 (three EGM and 1 Game Conversion)

        Sales Order: 2 EGM and 0 games
        QTY = 2 (two EGMs no games)

        Sales Order: 0 EGM and 12 games
        QTY = 12 (no EGMs and twelve game conversions)
    For NOW (June 2020) just add them both together
    """
    # List of items to display on the form
    formdata = []

    # How many new sales orders are there?
    numberofnewsalesorders = data['Pagination']['NumberOfItems']

    for item in data['Items']:
        order_number = item['OrderNumber'][7:]
        # retrieve Sales order info either locally or from item
        order = get_sales_order_info(order_number, item)

        model = None
        gamenames = []
        qty = 0

        for product in order.line_item.all():
            if product.code[:5] == 'EGMA3':
                qty += int(product.qty)
                model = product.code
            elif product.code[:4] == 'GAME':
                # ROB let's go and find the product in the database
                try:
                    game_name = UnleashedProductCode.objects.get(code=product.code)
                    gamenames.append(game_name.description)
                except:
                    gamenames.append('Unknown')
                qty += 1
            elif product.code[:3] == 'CRT':
                model = 'CRT'

        # We don't want to list products that start with CRT
        if (model != 'CRT'):
            row = {
                'order_number':  order_number,
                'customer_name': order.venue,
                'jurisdiction':  order.jurisdiction,
                'order_date':    order.order_date,
                'install_date':  order.install_date,
                'quantity':      str(qty),
                'model':         model,
                'games_list':    gamenames,
                'comments':      order.comment,
            }
            formdata.append(row)

    return formdata


def get_sales_order_info(order, data):
    """ This function will do one of two things
        Either find the order already in the local database
        OR
        create a new sales order entry in to the local database
        
        either way it will return the values needed
    """
    # Go and check to see if this order number already exists
    # in our database?
    # First implementation of seeing if orders exist in the local db
    #   stored_orders = UnleashedSalesOrder.objects.filter(order__contains=order_number)
    #   if stored_orders.exists():
    try:
        sales_order = UnleashedSalesOrder.objects.get(order__exact=order)
    except MultipleObjectsReturned:
        # We have more than one sales order with the same number
        # This should never be possible. Every sales order is unique
        print("[ERROR] sale/views.py: 202; Multiple sales order with the same number")
        sales_order = UnleashedSalesOrder(
            order=0,
            venue="Invalid",
            jurisdiction="Invalid",
            order_date="1 Jan 1970",
            install_date="1 Jan 1970",
            comment="Error duplicate Unleashed sales order numbers found in local db!",)
        sales_order.save()
    except ObjectDoesNotExist:
        customer = data['Customer']['CustomerName']
        jurisdiction = data['DeliveryRegion']
        comments = data['Comments']
        unleasheddate_str = data['OrderDate'][6:-2]
        unleasheddate_int = int(unleasheddate_str[:10])
        order_date = date.fromtimestamp(unleasheddate_int).strftime('%d %b %Y')
        unleasheddate_str = data['RequiredDate'][6:-2]
        unleasheddate_int = int(unleasheddate_str[:10])
        reqd_date = date.fromtimestamp(unleasheddate_int).strftime('%d %b %Y')

        # Create an Unleashed Sales Order
        sales_order = UnleashedSalesOrder(
            order=order,
            venue=customer,
            jurisdiction=jurisdiction,
            order_date=order_date,
            install_date=reqd_date,
            comment=comments,)
        sales_order.save()

        for line_item in data['SalesOrderLines']:
            item = UnleashedLineItem(
                code=line_item['Product']['ProductCode'],
                qty=int(line_item['OrderQuantity']),
                description=line_item['Product']['ProductDescription']
                )
            item.save()
            sales_order.line_item.add(item)

    return sales_order