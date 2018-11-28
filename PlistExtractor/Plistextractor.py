import os
import sqlite3
import datetime
import shutil
import argparse

def search(dirname, extract_dir, db_name):
    try:
        list_filename = os.listdir(dirname)
        for filename in list_filename:
            full_filename = os.path.join(dirname, filename)
            if os.path.islink(full_filename):
                continue
            if os.path.isdir(full_filename):
                search(full_filename, extract_dir, db_name)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.plist' or ext == '.sfl' or ext == '.sfl2' or ext == '.Shortcuts':
                    print(full_filename)
                    get_plist_metadata(full_filename, extract_dir, db_name)
                    try:
                        os.makedirs(extract_dir + os.path.dirname(full_filename))
                    except:
                        continue
                        
                    shutil.copyfile(full_filename, extract_dir + full_filename)

    except OSError as e:
        pass

def get_plist_metadata(full_filename, extract_dir, db_name):
    try:
        stat = os.stat(full_filename)
        conn = sqlite3.connect(extract_dir + "/" + db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO plist_metadata VALUES (?, ?, ?, ?, ?)",
                       (full_filename, stat.st_birthtime, stat.st_atime,
                        stat.st_mtime, stat.st_ctime))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass

def initialize_db(extract_dir_name, db_name):
    try:
        conn = sqlite3.connect(extract_dir_name + "/" + db_name)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS plist_metadata "
                       "(path TEXT, create_date INTEGER, access_date INTEGER, modify_date INTEGER, "
                       "entry_modify INTEGER)")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print("Can't create database : ", e.args[0])

def print_usage():
    print("-- Usage --")
    print("python Plistextractor.py -i /Volumes/[Volume] -o [Output path]")

def main():
    print("PlistExtractor v1.0")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input volume")
    parser.add_argument("-o", "--output", help="output directory for extract plist")
    args = parser.parse_args()

    volume_path = args.input
    extract_dir = args.output

    os.mkdir(extract_dir)

    db_name = str(datetime.datetime.now()) + ".db"

    initialize_db(extract_dir, db_name)

    search(volume_path, extract_dir, db_name)

main()