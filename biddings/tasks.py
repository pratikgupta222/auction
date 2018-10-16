from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from auction_site.celery import app
from biddings.utils import get_auctions_result, start_auction_for_items
from biddings.constants import AUCTION_MAIL_SUBJECT, WINNER_MAIL_BODY, REST_BIDDER_MAIL_BODY


@periodic_task(run_every=(crontab(hour="0,4,8,12,16,20,18", minute="15")))
def start_auction():
    start_auction_for_items()


@app.task
def send_auction_mail(user_ids, winner, final_price, item):
    UserModel = get_user_model()
    newline_delimiter = '<br>'

    subject = AUCTION_MAIL_SUBJECT.format(item_name=item)

    for user_id in user_ids:
        try:
            user = UserModel.objects.get(pk=user_id)
            if user == winner:
                html_content = WINNER_MAIL_BODY.format(
                    item_name=item, newline_delimiter=newline_delimiter)
            else:
                html_content = REST_BIDDER_MAIL_BODY.format(item_name=item,
                                                            final_amount=final_price,
                                                            winner_name=winner.name,
                                                            newline_delimiter=newline_delimiter)

                mail = EmailMultiAlternatives(
                    subject, html_content, to=user.email, from_email=settings.EMAIL_HOST_USER)
            mail.send()

        except UserModel.DoesNotExist:
            pass


@periodic_task(run_every=(crontab(hour="23", minute="00")))
def auction_completion():
    """Scheduled job at 4:30 AM to find the winner of each auction whose end_time is completed."""

    auction_list = get_auctions_result()

    if auction_list:
        for detail in auction_list:
            send_auction_mail.delay(detail.get('users_ids'),
                                    detail.get('winner'),
                                    detail.get('final_price'),
                                    detail.get('item'))
