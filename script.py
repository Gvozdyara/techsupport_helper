import pickle
import datetime

begin_time = datetime.datetime.now()

with open("techsupport_base", "rb") as f:
    Data_base = pickle.load(f)


result_string = str()
for i in Data_base:
    result_string += Data_base[i][0]


with open("sum_descr.txt", "w", encoding="utf8") as f:
    f.write(result_string)


end_time = datetime.datetime.now()

print(end_time - begin_time)