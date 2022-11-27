# -*- coding: utf-8 -*-
import argparse
import asyncio
import time
import sys
import os
from datetime import (datetime, date)
from pytz import UTC

from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import (
    Channel, Post
)

# import Telegram API submodules
from telegram_api import *

parser = argparse.ArgumentParser(description='Arguments.')
parser.add_argument(
    '--telegram-channel',
    type=str,
    required='--batch-file' not in sys.argv,
    help='Specifies a Telegram Channel.'
)
parser.add_argument(
    '--batch-file',
    type=str,
    required='--telegram-channel' not in sys.argv,
    help='File containing Telegram Channels, one channel per line.'
)

parser.add_argument(
    '--min-date',
    type=date.fromisoformat,
    help='Specifies min date'
)

# Parse arguments
args = vars(parser.parse_args())

if all(i is not None for i in args.values()):
    parser.error('Select either --telegram-channel or --batch-file options only.')


text = f'''
Start parsing at {time.ctime()}

'''
print (text)

# Telegram initialization
sfile = 'session_file'
config = ConfigParser()
config.read('./config/config.ini')

telegram_credentials = config['Telegram API credentials']

api_id = telegram_credentials['api_id']
api_hash = telegram_credentials['api_hash']
phone = telegram_credentials['phone']

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# loop = asyncio.get_event_loop()

client = loop.run_until_complete(
    get_connection(sfile, api_id, api_hash, phone)
)

# DB initialization
engine = create_engine(f"sqlite:///data/tchannels_narratives.db")
session = Session(engine)

if args['telegram_channel']:
    channels = [args['telegram_channel']]
elif args['batch_file']:
    channels = [
        i.rstrip() for i in open(
            args['batch_file'], encoding='utf-8', mode='r'
        )
    ]
else:
    channels = []

min_date = UTC.localize(args['min_date'] or datetime.fromisoformat('2022-01-01'))

print(min_date)

for channel_name in channels:
    print ('')
    print (f'> Collecting data from Telegram Channel -> {channel_name}')
    print ('> ...')
    print ('')

    # Channel's attributes
    challenge_info = loop.run_until_complete(
        get_entity_attrs(client, channel_name)
    )

    channel_id = challenge_info.id

    # Collect Source -> GetFullChannelRequest
    channel_details = loop.run_until_complete(
        full_channel_req(client, channel_id)
    )

    # save data
    print ('> Saving channel data...')
    channel_entry = session.query(Channel).filter_by(id=channel_id).first()
    if not channel_entry:
        channel_entry = Channel(
            id=channel_id,
            username=channel_name,
            description=channel_details.full_chat.about
        )
        session.add(channel_entry)
    print ('> done.')
    print ('')

    # Collect posts
    posts = loop.run_until_complete(
        get_posts(client, channel_id)
    )

    print (f'> Collecting messages from {posts.messages[-1].date} to {posts.messages[0].date} Telegram Channel -> {channel_name}')

    for message in posts.messages:
        post_entry = session.query(Post).filter_by(id=message.id).first()
        if not post_entry:
            post_entry = Post(
                id=message.id,
                channel_id=channel_id,
                message=message.message,
                posted_at=message.date
            )
            session.add(post_entry)

    session.commit()

    offset_id = posts.messages[-1].id
    offset_date = posts.messages[-1].date

    while len(posts.messages) > 0 and offset_date > min_date:
        posts = loop.run_until_complete(
            get_posts(client, channel_id, offset_id=offset_id)
        )

        print (f'> Collecting messages from {posts.messages[-1].date} to {posts.messages[0].date} Telegram Channel -> {channel_name}')

        for message in posts.messages:
            post_entry = session.query(Post).filter_by(id=message.id).first()
            if not post_entry:
                post_entry = Post(
                    id=message.id,
                    channel_id=channel_id,
                    message=message.message,
                    posted_at=message.date
                )
                session.add(post_entry)

        session.commit()

        offset_id = posts.messages[-1].id
        offset_date = posts.messages[-1].date

    session.commit()

    print ('> done.')
    print ('')

    # sleep program for a few seconds
    if len(channels) > 1:
        time.sleep(60)


# log results
text = f'''
End parsing at {time.ctime()}

'''
print (text)
