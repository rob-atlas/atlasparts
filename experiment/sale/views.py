import os
import requests
from datetime import date

from django.shortcuts import render
from django.http import HttpResponse

from .unleashed.auth import UnleashedAuth


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
    load information either from unleashed url
    Using the API id & key from environment variables
    We will get back a json file if successful
    or we return a text string with the error
    """
    data = None

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
    This function extracts from the data only the items we are interested in
    for displaying on the webpage
    """
    productcodes = {
        'GAMENSW001': 'Buffalo Bucks',
        'GAMENSW002': 'Incredible Phoenix',
        'GAMENSW003': 'Gorilla Wins',
        'GAMENSW004': 'Lucky Packet',
        'GAMENSW005': 'Fortune Lantern',
        'GAMENSW006': "Giant's Jackpot",
        'GAMENSW007': 'Black Samurai',
        'GAMENSW008': 'Chilli Kings',
        'GAMENSW009': 'Treasure Stacks',
        'GAMENSW010': 'Treasure Gods',
        'GAMENSW011': 'Pharaohs Gods',
        'GAMENSW012': 'Wu Xing Fa',
        'GAMENSW013': 'China League',
        'GAMENSW014': 'Acropolis Diamond Pays',
        'GAMENSW015': 'Angkor Gold Diamond Pays',
        'GAMENSW016': "'Dragons's Gate Diamond Pays",
        'GAMENSW017': 'League of Ages',

        'GAMESAC007': 'Black Samurai',
        'GAMESAC0026': 'Treasure Gods',
        'GAMESAC029': 'Chilli Kings',
        'GAMESAC036': 'Buffalo Bucks',
        'GAMESAC0050': 'Pharaohs Gods',
        'GAMESAC055': 'China League',

        'GAMEVIC0026': 'Treasure Gods',
        'GAMEVIC0032': 'Gorilla Wins',
        'GAMEVIC0036': 'Buffalo Bucks',
        'GAMEVIC0043': 'Incredible Phoenix',
        'GAMEVIC029': 'Chilli Kings',
        'GAMEVIC049': 'Treasure Stacks',
        'GAMEVIC0050': 'Pharaohs Gods',
        'GAMEVIC0052': 'Black Samurai',
        'GAMEVIC055': 'China League',

        'GAMENSW001': 'Incredible Phoenix',
        'GAMENSW002': 'Treasure Gods',
    }

    formdata = []
    # How many new sales orders are there?
    numberofnewsalesorders = data['Pagination']['NumberOfItems']

    for item in data['Items']:
        model = None
        gamenames = []
        egms = str(0)
        for line_item in item['SalesOrderLines']:
            product = line_item['Product']['ProductCode']
            if product[:5] == 'EGMA3':
                # check for how many machines
                egms = str(int(line_item['OrderQuantity']))
                model = product
            elif product[:4] == 'GAME':
                if product in productcodes:
                    gamenames.append(productcodes[product])
                else:
                    gamenames.append('Unknown')
            elif product[:4] == '26-':
                ptm = product

        f = item['OrderDate'][6:-2]
        d = int(f[:10])
        order_date = date.fromtimestamp(d).strftime('%d %b %Y')
        f = item['RequiredDate'][6:-2]
        d = int(f[:10])
        reqd_date = date.fromtimestamp(d).strftime('%d %b %Y')

        row = {
            'order_number':  item['OrderNumber'][7:],
            'customer_name': item['Customer']['CustomerName'],
            'jurisdiction':  item['DeliveryRegion'],
            'order_date':    order_date,
            'install_date':  reqd_date,
            'quantity':      egms,
            'model':         model,
            'games_list':    gamenames,
            'comments':      item['Comments'],
        }
        formdata.append(row)

    return formdata
