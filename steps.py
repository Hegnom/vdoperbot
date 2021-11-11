
from telegram import ReplyKeyboardMarkup,Update, InlineKeyboardMarkup,ParseMode
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from varconf import *
from database import * 
from keyboards import *
#add video by user
def user_starter(update: Update, context: CallbackContext):
    update.message.reply_text('send -vdo-',reply_markup=ReplyKeyboardMarkup(cancell_keyboard,resize_keyboard=True))
    context.user_data["conv"] = True
    return USERVIDEO
def user_get_video(update: Update, context: CallbackContext):
    unique_id = []
    for i in vdo_result : 
        unique_id.append(i[2])
    if update.message.video.mime_type != "video/mp4":
        update.message.reply_text("the mime type isn't supported.\nUse (@webm2mp4bot) to change it to mp4.")
        return USERVIDEO
    if update.message.video.file_unique_id in unique_id : 
        update.message.reply_text('this video has already been added pls try another one ...')
        return USERVIDEO
    else:
        context.user_data['video_id'] = update.message.video.file_id
        context.user_data['video_unique_id']= update.message.video.file_unique_id
        update.message.reply_text('send the name you want -vdo- to be called.')
        return USERTAGS

def user_get_tags_and_verifier (update: Update, context: CallbackContext):
    last_uid = vdo_result[-1][0]
    if len(update.message.text)> 64 : 
        update.message.reply_text('The name is too long try some thing smaller than 64 ')
        return USERTAGS
    else :
        context.user_data['tags']= update.message.text     
        try:
            val = ( 
                str(eval(last_uid)+1),
                context.user_data['video_id'],
                context.user_data['video_unique_id'],
                context.user_data['tags'],
                'False',
                str(update.effective_user.id)
                )
            db.insert_vdo(val)
            caption= update.effective_user.mention_html()+" | "+context.user_data['tags'] 

            context.bot.send_video(chat_id=VERIFICATIONCHANNEL,
                               video = context.user_data['video_id'],
                               caption=caption,reply_markup =InlineKeyboardMarkup(keyboard),
                               parse_mode=ParseMode.HTML)
            context.bot.send_message(chat_id=update.effective_user.id , text ="wait till we verify ... ",
                                        reply_markup=ReplyKeyboardMarkup(main_keyboard,resize_keyboard=True))
        except:
            context.bot.send_message(chat_id=update.effective_user.id,text="pls try later or contact @Hegnom",
                                        reply_markup=ReplyKeyboardMarkup(main_keyboard,resize_keyboard=True))
        context.user_data["conv"]= False
        return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) :
    update.message.reply_text('ok see you later',
                                    reply_markup=ReplyKeyboardMarkup(main_keyboard,resize_keyboard=True))
    context.user_data["conv"]= False
    return ConversationHandler.END
