import ftplib
import os.path
from utils.config import *
from utils.classification_image import Classification_Image
import psycopg2
import json



def connect_ftp():
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.set_pasv(True)
    ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)
    return ftp


def check_and_create_directory(ftp, directory):
    try:
        ftp.cwd(directory)
    except ftplib.error_perm as e:
        if str(e).startswith('550'):
            ftp.mkd(directory)
        else:
            print(f"Error changing to directory '{directory}': {e}")


def download_file(ftp, ftp_file_path, local_file_path):
    try:
        with open(local_file_path, 'wb') as file:
            ftp.retrbinary(f"RETR {ftp_file_path}", file.write)
        print(f"Downloaded '{ftp_file_path}' to '{local_file_path}'")
    except ftplib.all_errors as e:
        print(f"FTP error: {e}")


def route_to_db(cursor):
    cursor.execute('SET search_path TO public')
    cursor.execute("SELECT current_schema()")


class Classification:
    def __init__(self):
        pass

    def classify(self, conn, id, task_param, model, scaler):
        src_img_path = task_param['input_file']
        try:
            filename = src_img_path.split("/")[-1]
            local_file_path = LOCAL_SRC_CLASSIFY_IMAGE_PATH + filename
            ftp = connect_ftp()
            download_file(ftp, src_img_path, local_file_path)
            classification_image = Classification_Image()
            result = classification_image.classify(local_file_path, model, scaler)
            task_output = {
                "output_class": result
            }
            print("Connection closed")
            cursor = conn.cursor()
            route_to_db(cursor)
            cursor.execute("UPDATE avt_task SET task_stat = 1, task_output = %s WHERE id = %s", (task_output, id,))
            conn.commit()
        except ftplib.all_errors as e:
            cursor = conn.cursor()
            route_to_db(cursor)
            cursor.execute("UPDATE avt_task SET task_stat = 0 WHERE id = %s", (id,))
            conn.commit()
            print(f"FTP error: {e}")

    def process(self, id, model, scaler):
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute('SET search_path TO public')
        cursor.execute("SELECT current_schema()")
        cursor.execute("SELECT * FROM avt_task WHERE id = %s", (id,))
        result = cursor.fetchone()
        classification = Classification()
        task_param = json.loads(result[5])
        classification.classify(conn, id, task_param, model, scaler)
        cursor.close()
