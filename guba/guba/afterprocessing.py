import pickle
import pymongo
from stocks_list import STOCKS_LIST

host = "127.0.0.1"
port = 27017

client = pymongo.MongoClient(host, port)
db_name_1 = "YQ_BASE"
db_name_2 = "YQ_OUTPUT"
col_raw = client[db_name_1]["GUBA_RAW"]
col_d = client[db_name_1]["GUBA_D_20170806"]
col_output = client[db_name_2]["OUTPUT_20170806"]


for stock in STOCKS_LIST:
	show_d = col_d.find({"ID":stock}, {"_id" : 0}) 
	items = list(show_d)
	post_add = 0
	read_add = 0
	comment_add = 0
	content_charactor_count = 0
	comments_charactor_count = 0
	faces_count = 0       
	for item in items:
		print(item)
		raw_querry = {"ID":item["ID"], "TITLE":item["TITLE"], "TIME":item["TIME"],  
			         "WRITER":item["WRITER"]}
		show_raw = col_raw.find(raw_querry, {"_id":0, "READ":1, "COMMENT":1})

		if show_raw.count() == 0:
			post_add += 1
			read_old = 0
			comment_old =0
			doc = {"ID":item["ID"], "TITLE":item["TITLE"], "TIME":item["TIME"], "WRITER":item["WRITER"],
					"READ":item["READ"], "COMMENT":item["COMMENT"],}
			col_raw.insert_one(doc)
		else:
			post = list(show_raw)[0]
			read_old = post["READ"]
			comment_old = post["COMMENT"]
			col_raw.update_one(raw_querry, {'$set' : {"READ" : item["READ"], "COMMENT": item["COMMENT"]}})

		try:
			for i in item["CONTENT"]:
				content_charactor_count += len(i)
		except:
			pass
			
		try:
			for i in item["COMMENTS"]:
				for j in i:
					comments_charactor_count += len(j)
		except:
			pass

		try:
			for i in item["FACE"]:
				faces_count += len(i)
		except:
			pass



		read_add += int(item["READ"]) - int(read_old)
		comment_add += int(item["COMMENT"]) - int(comment_old)

		doc = {"ID":item["ID"], "POST_ADD": post_add, "READ_ADD":read_add, "COMMENT_ADD":comment_add, 
				"CONTENT_C":content_charactor_count, "COMMENTS_C":comments_charactor_count, 
				"FACE_C":faces_count}

		col_output.insert_one(doc)





#评论：平均字数， 空评论数， 长评论数
#表情： 表情个数及占比，正负面表情个数及占比 

