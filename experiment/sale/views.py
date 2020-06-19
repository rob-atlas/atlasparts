import os
import requests
from datetime import date

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views import generic

from .unleashed.auth import UnleashedAuth

# ROB: not sure if that is how it is done but I want to
#      look up the Unleashed product code and get the game name back
from catalog.models import UnleashedProductCode, Jurisdiction
from .models import UnleashedSalesOrder, UnleashedLineItem

# Create your views here.
def index(request):
    if request.method == "POST":
        context = { 'data': 'Here is some info on the sales order' }
        template = 'sale/sale.html'
    else:
        info = get_unleashed_data()
        if isinstance(info, str):
            # An error occurred
            context = { 'data': info }
            template = 'sale/sale.html'
            return render(request, template, context)

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
        data = "Unable to get information from Unleashed" \
               + "\nReturned error code: " + str(r.status_code) \
               + "(" + requests.status_codes._codes[r.status_code][0] \
               + ")\nMost likely a connection timeout"

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

        # Only list products that don't start with CRT
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
        street = data['DeliveryStreetAddress']
        town = data['DeliveryCity']
        if town is None:
            town = data['DeliverySuburb']
        deliverystate = data['DeliveryRegion']
        pcode = data['DeliveryPostCode']
        comments = data['Comments']
        unleasheddate_str = data['OrderDate'][6:-2]
        unleasheddate_int = int(unleasheddate_str[:10])
        order_date = date.fromtimestamp(unleasheddate_int).strftime('%d %b %Y')
        unleasheddate_str = data['RequiredDate'][6:-2]
        unleasheddate_int = int(unleasheddate_str[:10])
        reqd_date = date.fromtimestamp(unleasheddate_int).strftime('%d %b %Y')

        deliveryname = data['DeliveryName']
        if deliveryname == None:
            deliveryname = customer

        customer_ref = data['CustomerRef']

        egm = None
        for line_item in data['SalesOrderLines']:
            if line_item['Product']['ProductCode'][:3] == 'EGM':
                egm = line_item['Product']
                break

        if deliverystate == None and town == None and egm['ProductCode'] != None:
            deliverystate = egm['ProductCode'][5:8]
        jur = get_jurisdiction(deliverystate, deliveryname, town, egm)

        # Create an Unleashed Sales Order
        sales_order = UnleashedSalesOrder(
            order=order,
            venue=customer,
            address=street,
            town=town,
            state=deliverystate,
            postcode=pcode,
            jurisdiction=jur,
            order_date=order_date,
            install_date=reqd_date,
            comment=comments,
            customer_reference=customer_ref,
            delivery_name=deliveryname,
            )
        sales_order.save()

        # add each line item to the sales order
        for line_item in data['SalesOrderLines']:
            item = UnleashedLineItem(
                code=line_item['Product']['ProductCode'],
                qty=int(line_item['OrderQuantity']),
                description=line_item['Product']['ProductDescription']
                )
            item.save()
            sales_order.line_item.add(item)

    return sales_order

def get_jurisdiction(state, delivery, city, machine):
    """ Function tries to decipher what jurisdiction the sales order
        belongs to
        attributes:
            state = if known what state the venue is located in eg Victoria
            delivery = where the product needs to be shipped to likely
            city = location of the suburb/city
            machine_number = if a machine is being ordered we can work out
    """
    jur = "ROB"
    if machine:
        p_code, created = UnleashedProductCode.objects.get_or_create(
            code=machine['ProductCode'],
            defaults={'description': machine['ProductDescription']},
        )
        if created == False:
            jur = p_code.code[5:8]
        else:
            jur = "Need more look ups"
    elif state:
        # We know the state but not which jurisdiction specifically
        # Let's do a lookup
        try:
            query = Jurisdiction.objects.filter(name__startswith=state)[0]
            jur = query.name
            import pdb; pdb.set_trace()
        except:
            query = "NSW-ROB"
            jur = state
    elif delivery:
        jur = delivery
    elif city:
        jur = delivery
    else:
        jur = "Unknown"

    return jur


class UnleashedSalesOrderView(generic.DetailView):
    model = UnleashedSalesOrder
