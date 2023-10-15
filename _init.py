import base64


if __name__ == '__main__':
    pw = 'saw$dwA#wk@S54'
    urlsafe = base64.urlsafe_b64encode(pw.encode('utf-16le'))

    print(urlsafe)
