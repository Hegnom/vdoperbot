

from telegram.ext import CallbackContext, ConversationHandler
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup,ParseMode
from varconf import *
from steps import *
from functions import *
from messages import *
from keyboards import *

def start(update: Update, context: CallbackContext) -> None:
    try : 
        if context.user_data["conv"] == True :
            ConversationHandler.END
            context.user_data["conv"]=False
        if context.user_data["conv"] == False:
            pass
    except: 
        pass
    finally:
        user = update.effective_user
        start =(fr"Hi {user.mention_markdown_v2()} \!")+welcome
        update.message.reply_markdown_v2(start,reply_markup=ReplyKeyboardMarkup(main_keyboard,resize_keyboard=True))

def info(update: Update, context: CallbackContext) :
    try:
        update.message.reply_text(help_Txt , parse_mode=ParseMode.HTML)
    except:
        pass
def help (update: Update, context: CallbackContext):
    update.message.reply_text("In order to use, You have to choose one or type bot id(@vdoperbot).",
                              reply_markup= InlineKeyboardMarkup(help_key_board) )

def video_name(update: Update, context: CallbackContext):
    vdo_check = dict()
    for i in vdo_result:
        vdo_check.update({i[3]:i[2]})
    if update.message.video.file_unique_id in vdo_check: 
        key_board_3=[
                [InlineKeyboardButton('share video' , 
                    switch_inline_query =vdo_check[update.message.video.file_unique_id])
                    ],
                        ]
        update.message.reply_text("<b>vdo name:</b>\n[ <code>%s</code> ]"%vdo_check[update.message.video.file_unique_id],
                                    reply_markup=InlineKeyboardMarkup(key_board_3),
                                        parse_mode=ParseMode.HTML)

def chosen_inline(update: Update, context: CallbackContext):
    chosen= str(update.chosen_inline_result.result_id)
    uid = chosen.split("_")[0]
    try:
        uid_lis= context.user_data["recent"]
    except:
        uid_lis= []
    z= []
    for i in vdo_result:
        if uid in i[0]:
            z.append(i)
    uid_lis.extend(z)
    my_lis= list(reversed(list(dict.fromkeys(reversed(uid_lis)))))
    context.user_data["recent"]= my_lis

def channel_inlinekey(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    message= update.effective_message
    info= db.fetch_user_and_fileid(val= (message.video.file_unique_id))
    user_id= eval(info[4])
    if query.data == '1' :
        try:
            db.verify_updater(mod= 1 ,value= (message.video.file_unique_id))
            try :
                query.delete_message()
                key_board_3= [
                     [InlineKeyboardButton('share video' , switch_inline_query =info[2])],
                       ]
                context.bot.send_video(chat_id= CHANNEL, video =message.video.file_id ,
                                          caption=message.caption,parse_mode=ParseMode.HTML)
                #'SELECT uid , fileid, tags, fileuniqueid, userid
                vdo_result.extend([(info[0],info[1],info[2],info[3])])
                
                context.bot.send_message(chat_id= user_id, text= 'your -vdo- is accepted ✅',
                                           reply_markup= InlineKeyboardMarkup(key_board_3))
            except:
                pass
        except:
            pass
    if query.data == '2' :
        try :
            db.verify_updater(mod= 2,value= (message.video.file_unique_id))
            query.delete_message()
            context.bot.send_message(chat_id= user_id, text= "your vdo isn't accpeted ❌")
            
        except:
            pass
