import time
import os
from email.message import EmailMessage
import smtplib
from os import listdir
from os.path import isfile, join
import datetime
import shutil

BASE_PATH = "F:/nikhil/mobile/pics"
MOVE_TO = "F:/nikhil/mobile/sent"

file_name_mtime = [(file, os.stat(join(BASE_PATH, file)).st_mtime) for file in listdir(BASE_PATH) if isfile(join(BASE_PATH, file))]
sorted_file_names = sorted(file_name_mtime, key=lambda x:x[1])
MAX_ALLOWED_SIZE = 15500000
FILE_COUNT = len(file_name_mtime)
print(f"FILE_COUNT: {FILE_COUNT}")
EMAIL_COUNT = 0
username = str('nikhil_id2006@yahoo.com')
password = str('baefjwqfbhjlalfww')
move_dir_list = os.listdir(MOVE_TO)

for file_name, mtime in sorted_file_names:

    if file_name not in move_dir_list:
        file_path = join(BASE_PATH, file_name)
        file_size = os.stat(file_path).st_size
        mtime = os.stat(file_path).st_mtime
        month_year = datetime.datetime.fromtimestamp(mtime).strftime('%B-%Y')
        if file_size < MAX_ALLOWED_SIZE:
            print(f"Uploading file: {file_name}")
            with open(file_path, "rb") as fp:
                try:
                    server = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
                    # print("1111111111")
                    server.login(username, password)
                    print("Login done..")
                    msg = EmailMessage()
                    msg["Subject"] = f"Pics from mobile phone {month_year}"
                    msg["From"] = "nikhil_id2006@yahoo.com"
                    msg["To"] = "nikhil_id2006@yahoo.com"
                    msg.add_attachment(fp.read(), maintype="image", subtype="jpg")
                    server.send_message(msg)
                    # time.sleep(1)
                    print('ok the email has been sent')
                    EMAIL_COUNT += 1
                    print(EMAIL_COUNT)
                    shutil.copy2(file_path, join(MOVE_TO, file_name))
                    print("Copy done..")
                    server.quit()
                except Exception as ex:
                    print(ex)
                    time.sleep(200)
                    print("Wait done..")


print(f"EMAIL_COUNT: {EMAIL_COUNT}")
