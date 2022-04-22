import yadisk
import os
import datetime as dt

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
        return "techsupport_base"
    except yadisk.exceptions.PathNotFoundError:
        return False
    except:
        print("connection error")
        return False

def is_disk_more_fresh():
    file_mode_time_epoch = os.path.getmtime("techsupport_base")
    file_mode_time = dt.datetime.utcfromtimestamp(file_mode_time_epoch)
    with open("ya_id.txt", "r") as f:
        tok = f.read()
    y = yadisk.YaDisk(token=tok)
    try:
        resobj = y.get_meta("/TSH/techsupport_base")
        if resobj["modified"].replace(tzinfo=None) - file_mode_time >= dt.timedelta(seconds=5):
            return True
        else:
            return False
    except yadisk.exceptions.PathNotFoundError:
        return False
