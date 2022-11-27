import argparse

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import datetime
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
# from scipy.interpolate import make_interp_spline

from models import (Channel, Post)

engine = create_engine(f"sqlite:///data/tchannels_narratives.db")

parser = argparse.ArgumentParser(description='Arguments.')
parser.add_argument(
    '--telegram-channel',
    type=str,
    help='Filter by the Telegram Channel.'
)

parser.add_argument(
    '--narrative',
    type=str,
    help='Narrative (D - discrediting the authorities|H - humiliation of sculture)',
    required=True
)

parser.add_argument(
    '--from',
    type=date.fromisoformat,
    help='From date',
    required=True
)

parser.add_argument(
    '--to',
    type=date.fromisoformat,
    help='To date',
    required=True
)

# Parse arguments
args = vars(parser.parse_args())

# if all(i is not None for i in args.values()):
#     parser.error('Provide --from, --to and --narrative options. --telegram-channel is optional')

with Session(engine) as session:
    query = session.query(Post, sqlalchemy.func.count())

    if args['telegram_channel']:
        channel = session.query(Channel).filter_by(username=args['telegram_channel']).first()
        query = query.filter_by(channel_id=channel.id)

    if args['narrative'] == 'D':
        query = query.filter_by(discrediting_the_authorities_narrative=True)

    if args['narrative'] == 'H':
        query = query.filter_by(humiliation_of_culture_narrative=True)


    report = query.group_by(sqlalchemy.func.strftime("%Y-%m-%d", Post.posted_at)).order_by(Post.posted_at.asc()).all()
    report_hash = {}

    for item in report:
        report_hash[item[0].posted_at.strftime("%Y-%m-%d")] = item[1]

    dates = pd.date_range(start=args["from"], end=args["to"])

    sample_data = {
        'Date': dates,
        'Narrative frequence': [report_hash.get(date.strftime("%Y-%m-%d"), 0) for date in dates]
    }

    dataframe = pd.DataFrame(sample_data, columns=['Date', 'Narrative frequence'])

    dataframe["Date"] = dataframe["Date"].astype("datetime64[D]")
    dataframe = dataframe.set_index("Date")

    plt.style.use("fivethirtyeight")
    plt.figure(figsize=(12, 10))
    if args['narrative'] == 'D':
        plt.title('Дискредитація влади')
    if args['narrative'] == 'H':
        plt.title('Демонізація українців')

    plt.xlabel("Date")
    plt.ylabel("Narrative frequence")
    # plt.plot(dataframe["Disc"])
    # plt.show(block=True)

    plt.bar(dataframe.index, dataframe["Narrative frequence"], width=1)
    plt.show(block=True)
