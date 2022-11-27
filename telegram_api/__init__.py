# -*- coding: utf-8 -*-

# import Telethon API modules
from telethon import TelegramClient, types
from telethon.tl.functions.channels import GetChannelsRequest, \
    GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest

async def get_connection(session_file, api_id, api_hash, phone):
    '''
    Connects to Telegram API
    '''
    client = TelegramClient(session_file, api_id, api_hash)
    await client.connect()
    if await client.is_user_authorized():
        print ('> Authorized!')
    else:
        print ('> Not Authorized! Sending code request...')
        await client.send_code_request(phone)
        await client.sign_in(
            phone,
            input('Enter the code: ')
        )

    return client


'''

Channels

'''

# get telegram channel main attrs 
async def get_entity_attrs(client, source):
    '''
    Source: entity (str | int | Peer | InputPeer)
        More on InputPeer: https://tl.telethon.dev/types/input_peer.html

    Reference:
        Telethon: https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.users.UserMethods.get_entity
        Output attrs: https://core.telegram.org/constructor/channel

    '''
    return await client.get_entity(source)

# get channel request
async def get_channel_req(client, source):
    '''
    Source: <ChannelInput>

    Reference:
        Telethon: https://tl.telethon.dev/methods/channels/get_channels.html
        Output attrs: https://core.telegram.org/constructor/chat
    '''
    if type(source) != list:
        source = [source]

    return await client(
        GetChannelsRequest(source)
    )

# get full channel request
async def full_channel_req(client, source):
    '''
    Source: <ChannelInput>

    Reference:
        Telethon: https://tl.telethon.dev/methods/channels/get_full_channel.html
        Output attrs: https://core.telegram.org/constructor/messages.chatFull
    '''

    return await client(
        GetFullChannelRequest(source)
    )

'''

Messages

'''

# get posts
async def get_posts(client, source, min_id=0, offset_id=0):
    '''
    Source: entity (str | int | Peer | InputPeer)
        More on InputPeer: https://tl.telethon.dev/types/input_peer.html

    Reference:
        Telethon: https://tl.telethon.dev/methods/messages/get_history.html
        Output attrs: https://core.telegram.org/constructor/messages.channelMessages
    '''

    return await client(
        GetHistoryRequest(
            peer=source,
            hash=0,
            limit=100,
            max_id=0,
            min_id=min_id,
            offset_id=offset_id,
            add_offset=0,
            offset_date=0,
        )
    )
