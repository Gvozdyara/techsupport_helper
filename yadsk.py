import yadisk
import os
import datetime as dt
import requests

def upload():
    global y
    y = False
    with open("ya_id.txt", "r") as f:
        tok = f.read()
    y = yadisk.YaDisk(token=tok)
    print(y.check_token()) # Проверим токен
    y.upload("techsupport_base", "/TSH/techsupport_base", overwrite=True)





def download():
    try:
        with open("ya_id.txt", "r") as f:
            tok = f.read()
        y = yadisk.YaDisk(token=tok)
        # Download "/some-file-to-download.txt" to "downloaded.txt"
        y.download("/TSH/techsupport_base", "techsupport_base")
        return True
    except yadisk.exceptions.PathNotFoundError:
        return False
    except ConnectionError:
        print("connection error")
        return False

def is_cloud_more_fresh(var):
    global Data_base
    try:

        with open("ya_id.txt", "r") as f:
            tok = f.read()
        y = yadisk.YaDisk(token=tok)

        resobj = y.get_meta("/TSH/techsupport_base")
        file_mode_time_epoch = os.path.getmtime("techsupport_base")
        file_mode_time = dt.datetime.utcfromtimestamp(file_mode_time_epoch)
        if resobj["modified"].replace(tzinfo=None) - file_mode_time >= dt.timedelta(seconds=100):
            return True
        else:
            return False
    except yadisk.exceptions.PathNotFoundError:
        print("PathNotFoundError")
        return False
    except FileNotFoundError:
        return True
    except requests.exceptions.ConnectionError:
        print("connection error")
        var.set(0)
        return False

if __name__ == "__main__":
    file_mode_time_epoch = os.path.getmtime("techsupport_base")
    file_mode_time = dt.datetime.utcfromtimestamp(file_mode_time_epoch)
    with open("ya_id.txt", "r") as f:
        tok = f.read()
    y = yadisk.YaDisk(token=tok)
    try:
        resobj = y.get_meta("/TSH/techsupport_base")
        print(resobj["modified"].replace(tzinfo=None), "resobj")
        print(file_mode_time, "file_mode_time")
        print(dt.timedelta(seconds=5), "dt.timedelta(seconds=5)")
        print(resobj["modified"].replace(tzinfo=None) - file_mode_time, 'resobj["modified"].replace(tzinfo=None) - file_mode_time')
        print(file_mode_time-resobj["modified"].replace(tzinfo=None), 'file_mode_time-resobj["modified"].replace(tzinfo=None)')
        if resobj["modified"].replace(tzinfo=None) - file_mode_time < dt.timedelta(seconds=5):
            print ("True")
        else:
            print ("False")
    except yadisk.exceptions.PathNotFoundError:
        print ("exception")
