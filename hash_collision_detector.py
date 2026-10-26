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


for i in range(len(file_list)):

    for j in range(len(file_list)):

        if(i != j and (md5list[i] == md5list[j] and sha1list[i] == sha1list[j] and sha256list[i] != sha256list[j])):
            add_state(state_list, "sha1_and_md5_collision")
            print("md5 and sha1 collision", file_list[i])
            break

        elif(i != j and (md5list[i] == md5list[j] and sha1list[i] != sha1list[j])):
            add_state(state_list, "md5_collision")
            print("md5 collision", file_list[i])
            break

        elif(i != j and (md5list[i] != md5list[j] and sha1list[i] == sha1list[j])):
            add_state(state_list, "sha1_collision")
            print("sha1 collision", file_list[i])
            break

        elif(i != j and sha256list[i] == sha256list[j]):
            add_state(state_list, "copy")
            print("file copy", file_list[i])
            break
    
    if(len(state_list)!=i+1):
        add_state(state_list, "unique")
        print("unique file", file_list[i])


assert(len(file_list) == len(state_list))







