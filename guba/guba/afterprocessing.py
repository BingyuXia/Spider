import pickle
import pymongo



show = self.col.find({"ID":item["ID"], "TITLE":item["TITLE"], "TIME":item["TIME"], \
    "WRITER":item["WRITER"]}, {"_id":0, "READ":1, "COMMENT":1})
if show.count() == 0:
    read_old = 0
    comment_old =0
    doc = {key:item[key] for key in item}
    self.col.insert_one(doc)
else:
    post = list(show)[0]
    read_old = post["READ"]
    comment_old = post["COMMENT"]
    show.update_one({'$set' : {"READ" : item["READ"], "COMMENT": item["COMMENT"]}})
read_add = item["READ"] - read_old
comment_add = item["COMMENT"] - comment_old
doc = {"ID":item["ID"], "READ":read_add, "COMMENT":comment_add}
self.col2.insert_one(doc)

#评论：平均字数， 空评论数， 长评论数
#表情： 表情个数及占比，正负面表情个数及占比 

