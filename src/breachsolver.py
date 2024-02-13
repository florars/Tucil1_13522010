import tkinter as tk
from tkinter import filedialog
import os
import time
import random

class Cell:
    def __init__(self, token, row, col):
        self.picked = False
        self.token = token
        self.row = row
        self.col = col

class Sequence:
    def __init__(self, seq, reward):
        self.seq = seq
        self.reward = reward

class Solves:
    def __init__(self, token_arr):
        self.sum_reward = 0
        str = ""
        for i in token_arr:
            str += i.token + " "
        self.str = str
        coordinates = []
        for i in token_arr:
            coordinates.append(i.col + ", " + i.row)
        self.coordinates = coordinates
    def add(self):
        global solver_arr
        solver_arr.append(self)

def readfromtxt(arr):
    print("1. Menggunakan file browser\n2. Input nama file")
    metode2 = int(input())
    while (metode2!=1 and metode2!=2):
        print("1. Menggunakan file browser\n2. Input nama file")
        metode2=int(input())
    if (metode2==1):
        root = tk.Tk()
        root.withdraw()
        pth = filedialog.askopenfilename()
    else:
        print("Masukkan nama file txt!")
        pth = os.path.dirname(os.path.abspath(__file__)) + "\\..\\test\\" + input() + ".txt"
    setting = open(pth,"r")
    global buffersize; buffersize = int(setting.readline())
    dimension = setting.readline().split()
    global height; height = int(dimension[1])
    global width; width = int(dimension[0])
    mat = [[Cell("",-1,-1) for _ in range (int(dimension[1]))] for _ in range (int(dimension[0]))]
    for i in range (int(dimension[1])):
        tokens = setting.readline().split()
        for j in range (int(dimension[0])):
            temp = Cell(tokens[j], str(i+1), str(j+1))
            mat[i][j] = temp
    numseqs = int(setting.readline())
    for i in range (numseqs):
        tempstr = setting.readline().strip('\n')
        tempreward = int(setting.readline())
        tempseq = Sequence(tempstr,tempreward)
        arr.append(tempseq)
    return mat

def readinput(arr):
    print("Jumlah token unik:")
    unique = int(input())
    print("Masukkan token:")
    tokens = input().split()
    print("Masukkan ukuran buffer:")
    global buffersize; buffersize = int(input())
    print("Masukkan ukuran matriks (row col):")
    dimension = input().split()
    global height; height = int(dimension[0])
    global width; width = int(dimension[1])
    mat = [[Cell("",-1,-1) for _ in range (int(dimension[1]))] for _ in range (int(dimension[0]))]
    for i in range (int(dimension[0])):
        for j in range (int(dimension[1])):
            temp = Cell(random.choice(tokens), str(i+1), str(j+1))
            mat[i][j] = temp
    print("Masukkan jumlah sekuens:")
    numseqs = int(input())
    print("Masukkan ukuran maksimal sekuens:")
    maxlength = int(input())
    for i in range (numseqs):
        templst = random.sample(tokens, random.randint(1, maxlength))
        tempstr = " ".join(templst)
        tempreward = random.randint(-100, 100)
        tempseq = Sequence(tempstr,tempreward)
        arr.append(tempseq)
    return mat

def generator(generated, length, buffermax, isHorizontal, matrix, m, n, row, col):
    matrix[row][col].picked = True
    generated.append(matrix[row][col])

    if (length<buffermax-1):
        if (isHorizontal):
           for i in range (n):
               if (matrix[row][i].picked == False):
                    generator(generated, length+1, buffermax, not isHorizontal, matrix, m, n, row, i)
        else:
           for i in range (m):
               if (matrix[i][col].picked == False):
                    generator(generated, length+1, buffermax, not isHorizontal, matrix, m, n, i, col)
    elif (length==buffermax-1):
        temp = Solves(generated)
        temp.add()

    matrix[row][col].picked = False
    if (len(generated)>0):
        del generated[-1]      

def compare(solver, sequence):
    maxscore = 0
    idx = -1
    for i in range (len(solver)):
        for j in sequence:
            if (j.seq in solver[i].str):
                solver[i].sum_reward += j.reward
        if ((solver[i].sum_reward > maxscore)):
            idx = i
            maxscore = solver[i].sum_reward
    return idx

buffersize = 0
maxscore = 0 
sequence_arr = []
solver_arr = []
height = 0
width = 0

print("Selamat datang di Breach Solver!")
print("Pilih metode input\n1. File txt\n2. CLI")
metode = int(input())
while (metode!=1 and metode!=2):
    print("Pilih metode input\n1. File txt\n2. CLI")
    metode=int(input())
if (metode==1):
    mat = readfromtxt(sequence_arr)
else:
    mat = readinput(sequence_arr)

print("Matriks yang akan dikerjakan:")
for i in range (height):
    for j in range (width):
        print (mat[i][j].token, end=" ")
    print("")
print("Sekuens:")
for i in sequence_arr:
    print(i.seq, end="      ")
    print(i.reward, end=" "); print("poin")

start=time.time()
for i in range (width):
    generator([], 0, buffersize, False, mat, height, width, 0, 0)
idx_sol = compare(solver_arr, sequence_arr)
end=time.time()

if (idx_sol == -1):
    print("Tidak ada solusi")
else:
    print("Solusi ditemukan!")
    print(solver_arr[idx_sol].sum_reward)
    print(solver_arr[idx_sol].str)
    for i in solver_arr[idx_sol].coordinates:
        print(i)
    print(round((end-start)*1000), "ms")

print("Simpan hasil ke file txt? (y/n)")
choice = input()
while (choice!="y" and choice!="n"):
    print("Simpan hasil ke file txt? (y/n)")
    choice = input()
if (choice=="y"):
    if (not os.path.isdir(os.path.dirname(os.path.abspath(__file__)) + "\\..\\test\\saved")):
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\..\\test\\saved")
    print("Masukkan nama file:")
    filename = os.path.dirname(os.path.abspath(__file__)) + "\\..\\test\\saved\\" + input() + ".txt"
    file = open(filename, "w")
    file.write(str(solver_arr[idx_sol].sum_reward) + "\n")
    file.write(solver_arr[idx_sol].str + "\n")
    for i in solver_arr[idx_sol].coordinates:
        file.write(i + "\n")
    file.write(str(round((end-start)*1000)) + " ms")
    file.close()
    print("File berhasil disimpan!")






