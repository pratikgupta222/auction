AUCTION_ONGOING = 'ongoing'
AUCTION_DONE = 'auctioned'
AUCTION_UPCOMING = 'upcoming'

AUCTION_MAIL_SUBJECT = """Result of the Auction for {item_name}"""
WINNER_MAIL_BODY = """
    Dear Sir/ Madam, {newline_delimiter}
    Greetings from Enguru! {newline_delimiter}{newline_delimiter}

    Your Bid for the auction of {item_name} is the highest.{newline_delimiter}
    Hence you have been Declared as the WINNER!!{newline_delimiter}{newline_delimiter}

    You will be receiving a mail with payment details. Kindly make the entire payment as per your bid.{newline_delimiter}{newline_delimiter}

    Once the payment is processed, the item will be delivered to your registered address within the following four working days. {newline_delimiter}{newline_delimiter}

    Regards, {newline_delimiter}
    Enguru Team
"""

REST_BIDDER_MAIL_BODY = """
    Dear Sir/ Madam, {newline_delimiter}{newline_delimiter}
    Greetings from Enguru! {newline_delimiter}{newline_delimiter}

    The auction of {item_name} has finally ended.{newline_delimiter}{newline_delimiter}

    Based on the bidding amount which was Rs.{final_amount}, {winner_name} has been selected as the winner.{newline_delimiter}{newline_delimiter}

    Thanks for placing the bid for the above item. Hope to see you soon in the next upcoming bid.{newline_delimiter}{newline_delimiter}

    For any query or clarification please get in touch with us. {newline_delimiter}{newline_delimiter}

    Regards, {newline_delimiter}
    Enguru Team
"""