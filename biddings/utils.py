from datetime import datetime
from biddings.models import AuctionItem
from biddings.constants import *


def validate_auction_item_data(params):
    response = {'success': False, 'errors': [], 'data': {}}
    start_time = None
    end_time = None

    if not params.get('name', None):
        response['errors'].append('Name for the item is needed')
    if not params.get('description', None):
        response['errors'].append('Description for the item is needed')
    if not params.get('image_url', None):
        response['errors'].append('Image URL for the item is needed')
    if not params.get('start_time', None):
        response['errors'].append('Start time for the auction is needed')
    else:
        try:
            start_time = datetime.strptime(
                params['start_time'], "%Y-%m-%d %H:%M:%S")

            if start_time < datetime.today():
                response['errors'].append('Start time cannot be before today')
        except Exception as e:
            response['errors'].append(e.args[0])

    if not params.get('end_time', None):
        response['errors'].append('End time for the auction is needed')
    else:
        try:
            end_time = datetime.strptime(
                params['end_time'], "%Y-%m-%d %H:%M:%S")

            if end_time < datetime.today() or (start_time and end_time < start_time):
                response['errors'].append(
                    'End time cannot be before today or the start time')

        except Exception as e:
            response['errors'].append(e.args[0])

    if response.get('errors'):
        return response

    response['success'] = True
    response['data'] = {
        'name': params['name'],
        'description': params['description'],
        'start_time': start_time,
        'end_time': end_time,
        'starting_amount': params['starting_amount'] if params.get('starting_amount', None) else 0.0,
        'image_url': params['image_url'],
        'status': "upcoming"

    }

    return response


def validate_bids_data(params):

    response = {'success': False, 'errors': [], 'data': {}}

    if not params.get('item_id'):
        response['errors'].append('Item id is needed')

    if not params.get('bid_by_id'):
        response['errors'].append("Bidder's User id is needed")

    if not params.get('amount'):
        response['errors'].append('Amount is needed')
    else:
        try:
            item = AuctionItem.objects.get(id=params['item_id'])

            if not item.start_time < datetime.now():
                response['errors'].append(
                    "Cannot bid for this item as Auction hasn't started yet")

            if item.end_time > datetime.now():
                response['errors'].append(
                    "Bidding has been freezed for this auction")

            if not params['amount'] > item.starting_amount:
                response['errors'].append(
                    'Amount Should be greater than or equal to the starting bid amount of the item')

        except:
            response['errors'].append('No such item exists')

    if response.get('errors'):
        return response

    response['success'] = True
    response['data'] = {
        'item_id': params['item_id'],
        'bid_by_id': params['bid_by_id'],
        'amount': params['amount']
    }

    return response


def get_auctions_result(auction_ids=None):
    current_time = datetime.now()
    auction_items = None
    auction_list = []
    if auction_ids:
        auction_items = AuctionItem.objects.filter(id__in=auction_ids,
                                                   end_time__lt=current_time,
                                                   status=AUCTION_ONGOING)
    else:
        auction_items = AuctionItem.objects.filter(end_time__lt=current_time,
                                                   status=AUCTION_ONGOING)

    if auction_items:
        for item in auction_items:
            max_bid = auction_item.bids_set.latest('amount')

            AuctionItem.objects.filter(id=item.id).update(
                winner=max_bid.bid_by, status=AUCTION_DONE)

            dict_ = {
                'final_price': max_bid.amount,
                'winner': max_bid.bid_by,
                'item': item.name,
                'users_ids': auction_item.bids_set.all().values_list('bid_by_id', flat=True)
            }

            auction_list.append(dict_)

    return auction_list


def start_auction_for_items(auction_item_ids=None):
    current_time = datetime.now()
    auction_items = None
    if auction_ids:
        auction_items = AuctionItem.objects.filter(id__in=auction_ids,
                                                   start_time__gt=current_time,
                                                   status=AUCTION_UPCOMING)
    else:
        auction_items = AuctionItem.objects.filter(start_time__gt=current_time,
                                                   status=AUCTION_UPCOMING)

    if auction_items:
        auction_items.update(status=AUCTION_ONGOING)
