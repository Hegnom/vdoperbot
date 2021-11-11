
from telegram import InlineKeyboardButton
cancell_keyboard = [['❌CANCEL']]
main_keyboard=[['➕VDO', 'USAGE'],['INFO']]
keyboard = [
        [
            InlineKeyboardButton('yes', callback_data='1'),
            InlineKeyboardButton('no', callback_data='2'),
        ],
    ]

help_key_board=[
         [InlineKeyboardButton('current chat inline query', switch_inline_query_current_chat ='')],
         [InlineKeyboardButton('other chat inline query' , switch_inline_query ='')]
       ] 
