# import pandas as pd
# import sqlite3
# from conf import load_in
# settings = load_in()
#
# con = sqlite3.connect(settings['USERS_DB'].format("Admin"))
# # pd.set_option('display.max_colwidth', -1)
# my_frame = pd.read_sql_query("SELECT hashtags, tweet, tweeted_time, user_name, user_description, user_handle FROM 'Thetable'", con)
# # print(my_frame)
# my_dict = my_frame.to_dict()
# clean_dict = {"Hashtags":{}, "Tweet":{}, "Time Tweeted":{}, "Tweeted By":{}}
# clean_dict['Hashtags'] = my_dict['hashtags']
# for i in range(len(my_dict['hashtags'])):
#     items = [my_dict['hashtags'][i],
#              my_dict['tweet'][i],
#              my_dict['tweeted_time'][i],
#              my_dict['user_name'][i],
#              my_dict['user_description'][i]]
#     if len(items[0]) == 0:
#         clean_dict["Hashtags"][i] = "None"
#     else:
#         clean_dict["Hashtags"][i] =  "  ".join(list(map(lambda y: "#"+y,items[0].strip('`').split('`'))))
#     clean_dict["Tweeted By"][i] = items[3]
#     clean_dict['Tweet'][i] = items[1]
#     clean_dict['Time Tweeted'][i] = items[2]
# print(clean_dict.items())
# x = my_frame.to_html()
# # print(x)
#
#
# x = "Stuff`Hey`Nice`"
# print(list(map(lambda y: "#"+y, x.strip('`').split('`'))))

x = [1,2,3,4]
y = [6,7,8,9]
z = [10, 11, 12, 13]

a = list(zip(x,y,z))
print(a)