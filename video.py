import logging
from telegram import Update,InlineQueryResultCachedVideo
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    InlineQueryHandler,
    CallbackQueryHandler,
    ChosenInlineResultHandler,
)
from uuid import uuid4
from searchengine import *
from varconf import *
from  steps import *
from functions import *
# Enable logging
logging.basicConfig(
    format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger= logging.getLogger(__name__)

def inlinequery(update:Update, context:CallbackContext):
    query= update.inline_query.query
    inline_results= list()
    try:
        recent= context.user_data["recent"]
    except : 
        recent= []
    try :
        results= search_engine(query,recent)
    except:
        results= [

            {
                    "uid":"nouid",
                    "tags":"wait till we fix :(",
                    "file_id":'BAACAgQAAxkBAAICcGC38ZIjHuMDOgsHru9UGcPyHMxzAAJhCgAC-O3AUbroA8GXMt0jHwQ'
            }
        ]
    for i in results :
            inline_results.append(InlineQueryResultCachedVideo( id= str(i["uid"])+"_"+str(uuid4()),
                                                                title= i["tags"],
                                                                video_file_id= i["file_id"]))
    update.inline_query.answer(inline_results,cache_time=0, switch_pm_text='Add -vdo-',
                                      switch_pm_parameter='addvideo', auto_pagination= True)

def main() :

    updater= Updater(TOKEN)

    dispatcher= updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start, run_async= True))
    user_conv= ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^➕VDO$"), user_starter, run_async= True) ],
        states= {
            USERVIDEO: [MessageHandler(Filters.video, user_get_video, run_async= True)],
            USERTAGS: [MessageHandler(Filters.text & ~Filters.command & ~Filters.regex(r"^❌CANCEL$"),user_get_tags_and_verifier, run_async=True)],        
        },
        fallbacks=[MessageHandler(Filters.regex(r"^❌CANCEL$"),cancel ,run_async=True)],  
    )
    dispatcher.add_handler(user_conv)

    dispatcher.add_handler(InlineQueryHandler(inlinequery, run_async=True))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^USAGE$"), help, run_async= True))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^INFO$"), info, run_async= True))
    dispatcher.add_handler(MessageHandler(Filters.video ,video_name, run_async= True))
    dispatcher.add_handler(CallbackQueryHandler(channel_inlinekey, run_async= True))
    dispatcher.add_handler(ChosenInlineResultHandler(chosen_inline))
    updater.start_polling()
    #updater.start_webhook(listen='0.0.0.0',port=443 ,url_path=TOKEN)
    #updater.start_webhook('http://eplick.xyz/'+TOKEN)
    updater.idle()
if __name__ == '__main__':
    main()