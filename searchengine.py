
from database import vdo_result ,db
#SELECT uid, fileid ,tags ,fileuniqueid 
def search_engine (query,recent) :
    search_lis= []
    query_string = str(query)
    myresult = vdo_result 
    if not vdo_result:
        db.video_fetch()
    if query == "":
        if not recent:
            for i in reversed(myresult):
                search_lis.append({"uid":i[0] , "file_id":i[1] , "tags":i[2]})
        else:
            myresult.extend(recent) 
            myresult = list(reversed(list(dict.fromkeys(reversed(myresult)))))
            for i in reversed(myresult):
                search_lis.append({"uid":i[0] , "file_id":i[1] , "tags":i[2]})
        
    else : 
        for i in reversed(myresult):
            if query_string.lower() in str(i[2]).lower() :
                search_lis.append({"uid":i[0] , "file_id":i[1] , "tags":i[2]})
            else :
                pass
    return search_lis