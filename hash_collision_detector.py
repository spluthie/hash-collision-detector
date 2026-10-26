import tkinter as tk
from tkinter import filedialog
import os
import hashlib

root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="Wybierz folder")
root.destroy()

file_list = os.listdir(folder_path)
file_list = [f for f in file_list if os.path.isfile(folder_path+'/' + f)]

md5list = []
sha1list = []
sha256list = []

def compute_file_hash(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


for i in range(len(file_list)):
    result = compute_file_hash(folder_path + '/' + file_list[i], 'md5')
    md5list.append(result)

    resut = compute_file_hash(folder_path + '/' + file_list[i], 'sha1')
    sha1list.append(resut)

    result = compute_file_hash(folder_path + '/' + file_list[i], 'sha256')
    sha256list.append(result)

assert len(file_list) == len(md5list) == len(sha1list) == len(sha256list)

ALLOWED_STATES = ["unique", "copy", "sha1_collision", "md5_collision", "sha1_and_md5_collision"]

def add_state(state_list, new_state):
    if new_state not in ALLOWED_STATES:
        raise ValueError("Incorrect state")
    state_list.append(new_state)

state_list = []


def detect_bad_bytes(filepath, filename1, filename2):


    with open(os.path.join(filepath, filename1), "rb") as file1:
        data_1 = file1.read()

    with open(os.path.join(filepath, filename2), "rb") as file2:
        data_2 = file2.read()

    try:
        data_1.decode('utf-8')
        data_2.decode('utf-8')
        is_text = True
    except UnicodeDecodeError:
        is_text = False

    if is_text:
    
        for i in range(min(len(data_1), len(data_2))):
            if(data_1[i] != data_2[i]):
                print("Error on line:  ", data_1[:i].count(b'\n')+1 ," offset: ",  i, " data: ", hex(data_1[i]), " / ", hex(data_2[i]))
    
        if(len(data_1) > len(data_2)):
            print("Excess data of file ", filename1)
            for i in range(len(data_2), len(data_1)):
                print("On line: ", data_1[:i].count(b'\n')+1, " offset: ", i, " data: ", hex(data_1[i]))
    
        if(len(data_1) < len(data_2)):
            print("Excess data of file ", filename2)
            for i in range(len(data_1), len(data_2)):
                print("On line: ", data_2[:i].count(b'\n')+1, " offset: ", i, " data: ", hex(data_2[i]))
    
    else:
            
        print("For files: ", filename1, ", ",filename2)
        for i in range(min(len(data_1), len(data_2))):
            if(data_1[i] != data_2[i]):
                print("Offset ", i, " Data: ", hex(data_1[i]), " /  ", hex(data_2[i]))
        
        if(len(data_1) > len(data_2)):
            print("Excess offset of file ", filename1, ": ")
            for i in range(len(data_2), len(data_1)):
                print("Offset: ", i, " data:", hex(data_1[i]))
        
        if(len(data_1) < len(data_2)):
            print("Excess offset of file ", filename2, ": ")
            for i in range(len(data_1), len(data_2)):
                print("Offset: ", i, " data:", hex(data_2[i]))




for i in range(len(file_list)):

    for j in range(len(file_list)):

        if(i != j and (md5list[i] == md5list[j] and sha1list[i] == sha1list[j] and sha256list[i] != sha256list[j])):
            add_state(state_list, "sha1_and_md5_collision")
            if(i<j):
                print("md5 and sha1 collision between ", file_list[i], " and ", file_list[j])
                detect_bad_bytes(folder_path, file_list[i], file_list[j])
            break

        elif(i != j and (md5list[i] == md5list[j] and sha1list[i] != sha1list[j])):
            add_state(state_list, "md5_collision")
            if(i<j):
                print("md5 collision between ", file_list[i], " and ", file_list[j])
                detect_bad_bytes(folder_path, file_list[i], file_list[j])
            break

        elif(i != j and (md5list[i] != md5list[j] and sha1list[i] == sha1list[j])):
            add_state(state_list, "sha1_collision")
            if(i<j):
                print("sha1 collision between ", file_list[i], " and ", file_list[j])
                detect_bad_bytes(folder_path, file_list[i], file_list[j])
            break

        elif(i != j and sha256list[i] == sha256list[j]):
            add_state(state_list, "copy")
            print(file_list[i], " is a copy of ", file_list[j])
            break
    
    if(len(state_list)!=i+1):
        add_state(state_list, "unique")
        print("unique file", file_list[i])


assert(len(file_list) == len(state_list))







