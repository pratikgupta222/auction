import json
import logging
# import datetime

from django import db

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from biddings.models import AuctionItem, Bids
from biddings.serializers import *
from biddings.constants import *
from biddings.utils import *


class AuctionDetails(views.APIView):
    """
        Retrieve or update the driver instance
    """
    permission_classes = (AllowAny, )

    def get(self, request, pk, format=None):
        """
            Returns the driver record data corresponding to the driver id
        """
        response = {'data': {}, 'error': ''}

        auction_item_qs = AuctionItem.objects.filter(id=pk)

        auction_item_qs = auction_item_qs.select_related(
            'winner')
        auction_item_qs = auction_item_qs.prefetch_related('bids_set')

        if not auction_item_qs:
            logging.info("Invalid Aution Item ID")
            return Response(data="Auction Item does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        auction_item = auction_item_qs.first()

        max_bid = auction_item.bids_set.latest('amount')

        response['data'] = {
            'name': auction_item.name,
            'description': auction_item.description,
            'image_url': auction_item.image_url
        }

        if auction_item.status == AUCTION_DONE:
            response['data']['winner'] = auction_item.winner.name,
            response['data']['final_price'] = max_bid.amount
        else:
            response['data']['max_price'] = max_bid.amount

        return Response(status=status.HTTP_200_OK,
                        data=response)


class AuctionList(views.APIView):
    """
        List all the filtered driver records or create a new record
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        """
            For fetching all the auction item 
        """

        logging.info(
            "Following is the request data for fetching driver list : %s"
            % str(request.GET))

        auction_item_qs = AuctionItem.objects.all().order_by('status')

        auction_item_qs = auction_item_qs.select_related(
            'winner')

        auction_serializer = AuctionItemSerializer(auction_item_qs, many=True)

        data = auction_serializer.data

        if data:
            return Response(status=status.HTTP_200_OK,
                            data=data)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data='No Auction Item found')

    def post(self, request):
        """
            For creating a new aution item
        """

        try:
            data = json.loads(request.body)
            logging.info("Request from the app : " + str(request.body))
        except:
            data = json.loads(request.data.dict())
            logging.info(
                "Request from the app dict : " + str(request.data.dict()))

        response_dict = {'status': False, "message": ''}

        validated_data = validate_auction_item_data(params=data)

        if not validated_data.get('success'):
            response_dict["message"] = validated_data.get('errors')
            return Response(data=response_dict,
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        with db.transaction.atomic():
            try:
                serializer = AuctionItemSerializer(
                    data=validated_data.get('data'))

                if serializer.is_valid():
                    logging.info(
                        "Going to the app serializer with data: %s", validated_data.get('data'))
                    try:
                        auction_item = serializer.save()

                    except Exception as e:
                        logging.info(
                            "Following error occured while creating vehicle : %s", e)
                        response_dict = {
                            "status": False,
                            "message": e.args[0]
                        }
                        return Response(data=response_dict,
                                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    logging.info(
                        "This is the serializer error : %s", serializer.errors)
                    response_dict = {
                        "status": False,
                        "message": serializer.errors
                    }
                    return Response(data=response_dict,
                                    status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logging.info("This is the exception : %s " % e)
                response_dict["message"] = e.args[0]
                return Response(data=response_dict,
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/html; charset=utf-8')

            response_dict = {
                "status": True,
                "message": "Auction Item created"
            }

            return Response(status=status.HTTP_200_OK,
                            data=response_dict)


class BidDetails(views.APIView):
    """
        Retrieve or update the driver instance
    """
    permission_classes = (AllowAny, )

    def get(self, request, pk, format=None):
        """
            Returns the driver record data corresponding to the driver id
        """
        response = {'data': {}, 'error': ''}

        bids_qs = Bids.objects.filter(id=pk)

        bids_qs = bids_qs.select_related(
            'item', 'bid_by')

        if not bids_qs:
            logging.info("Invalid Bid ID")
            return Response(data="Bid does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        bid = bids_qs.first()

        response['data'] = {
            'item': bid.item.name,
            'bid_by': bid.bid_by,
            'amount': bid.amount
        }

        return Response(status=status.HTTP_200_OK,
                        data=response)


class BidList(views.APIView):
    """
        List all the filtered driver records or create a new record
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        """
            For fetching all the auction item 
        """
        filter_data = {}

        query_params = request.GET.dict()

        if query_params.get('bidder_id'):
            filter_data['bid_by_id'] = query_params['bidder_id']

        if query_params.get('item_id'):
            filter_data['item_id'] = query_params['item_id']

        if filter_data:
            bids_qs = Bids.objects.filter(**filter_data)

        else:
            bids_qs = Bids.objects.all()

        bids_qs = bids_qs.select_related(
            'item', 'bid_by')

        bid_serializer = BidsSerializer(bids_qs, many=True)

        data = bid_serializer.data

        if data:
            return Response(status=status.HTTP_200_OK,
                            data=data)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data='No Bids found')

    def post(self, request):
        """
            For creating a new aution item
        """

        try:
            data = json.loads(request.body)
            logging.info("Request from the app : " + str(request.body))
        except:
            data = json.loads(request.data.dict())
            logging.info(
                "Request from the app dict : " + str(request.data.dict()))

        response_dict = {'status': False, "message": ''}

        validated_data = validate_bids_data(params=data)

        if not validated_data.get('success'):
            response_dict["message"] = validated_data.get('errors')
            return Response(data=response_dict,
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        with db.transaction.atomic():
            try:
                serializer = BidsSerializer(
                    data=validated_data.get('data'))

                if serializer.is_valid():
                    logging.info(
                        "Going to the app serializer with data: %s", validated_data.get('data'))
                    try:
                        bid = serializer.save()

                    except Exception as e:
                        logging.info(
                            "Following error occured while creating vehicle : %s", e)
                        response_dict = {
                            "status": False,
                            "message": e.args[0]
                        }
                        return Response(data=response_dict,
                                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    logging.info(
                        "This is the serializer error : %s", serializer.errors)
                    response_dict = {
                        "status": False,
                        "message": serializer.errors
                    }
                    return Response(data=response_dict,
                                    status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logging.info("This is the exception : %s " % e)
                response_dict["message"] = e.args[0]
                return Response(data=response_dict,
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/html; charset=utf-8')

            response_dict = {
                "status": True,
                "message": "Bid Submitted"
            }

            return Response(status=status.HTTP_200_OK,
                            data=response_dict)
