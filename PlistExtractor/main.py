import os
import subprocess
import time

import sqlite3
import biplist
import dicttoxml

def search(dirname, extract_dir):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if extract_dir in full_filename:
                continue
            if "/.Trash" in full_filename:
                continue
            if os.path.islink(full_filename):
                continue
            if "/PycharmProjects" in full_filename:
                continue

            if os.path.isdir(full_filename):
                os.makedirs(extract_dir + full_filename)
                search(full_filename, extract_dir)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.plist':
                    print(full_filename)
                    get_plist_metadata(full_filename, extract_dir)
                    convert_to_plist(full_filename, extract_dir)
                if ext == '.sqlite':
                    print(full_filename)
                    get_plist_metadata(full_filename, extract_dir)
                    convert_to_plist(full_filename, extract_dir)
                if ext == '.sfl2':
                    print(full_filename)
                    get_plist_metadata(full_filename, extract_dir)
                    convert_to_plist(full_filename, extract_dir)
                if ext == '.Shortcuts':
                    print(full_filename)
                    get_plist_metadata(full_filename, extract_dir)
                    convert_to_plist(full_filename, extract_dir)
    except PermissionError:
        pass

def convert_to_plist(full_filename, extract_dir):
    try:
        plist = biplist.readPlist(full_filename)
        #print(plist)
        with open(extract_dir + full_filename, 'wb') as plist_temp:
            biplist.writePlist(plist, plist_temp.name, False)
    except:
        subprocess.Popen(
            ['plutil', '-convert', 'xml1', full_filename, '-o', extract_dir+full_filename],
            stdout=subprocess.PIPE)
        pass

def get_plist_metadata(full_filename, extract_dir):
    try:
        stat = os.stat(full_filename)
        db_name = extract_dir + ".db"
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO plist_metadata VALUES (?, ?, ?, ?, ?)",
                       (full_filename, stat.st_birthtime, stat.st_atime,
                        stat.st_mtime, stat.st_ctime))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print("Can't get plist metadata")
        pass

def initialize_db(extract_dir_name):
    db_name = extract_dir_name + ".db"

    try:
        print(db_name)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS plist_metadata "
                       "(path TEXT, create_date INTEGER, access_date INTEGER, modify_date INTEGER, "
                       "entry_modify INTEGER)")
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print("Can't create database : ", e.args[0])

def main():
    print("PlistExtractor v1.0")
    print("Target Volume List")
    diskutil_p = subprocess.Popen(['ls', '/Volumes'], stdout=subprocess.PIPE)
    diskutil_o = diskutil_p.stdout.read()
    print(diskutil_o)
    volume = input("input target volume : ")
    volume_path = "/Volumes/" + volume

    extract_dir = os.getcwd() + "_" + str(time.time())
    initialize_db(extract_dir)

    search(volume_path, extract_dir)

main()