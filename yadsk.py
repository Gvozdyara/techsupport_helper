import yadisk

def upload():
    global y
    y = False
    with open("ya_id.txt", "r") as f:
        tok = f.read()
    y = yadisk.YaDisk(token=tok)
    print(y.check_token()) # Проверим токен
    y.upload("techsupport_base", "/TSH/techsupport_base", overwrite=True)
    return


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
