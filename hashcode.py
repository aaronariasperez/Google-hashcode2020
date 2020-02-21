# Script for Google's Hashcode 2020
# Copyright (C) 2020  Aarón Arias Pérez & José Crespo Guerrero
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import sys
import os.path
import math
import random

def assert_input():
     if len(sys.argv) < 2:
        print("Script arguments are chungos. Usage: $ python3 script.py inputnamefile.txt")
        exit()
     if not os.path.exists(sys.argv[1]):
        print(sys.argv[1], "no existe ompare, no me la cuelas")
        exit()   
     if not os.path.isfile(sys.argv[1]):
        print(sys.argv[1], "está ma duro que zu puta madre... pa mi que ezo no es un fichero")
        exit()

def write_output(libraries):
    
    print(len(libraries))
    
    for library in libraries:
        books = library.books
        print(library.get_id(),len(books))
        print(*books)

class Library:
    def __init__(self, num, books, signup, perDay):
        self.num = num
        self.books = books
        self.signup = signup
        self.perDay = perDay
    def get_id(self):
        return self.num
    def get_books(self):
        return self.books.copy()
    def get_signup(self):
        return self.signup
    def get_perDay(self):
        return self.perDay

def shuffle_all(libraries):
    random.shuffle(libraries)
    for library in libraries:
        random.shuffle(library.books)

def cooling(T):
    return 0.95*T

def swap(array, tupla):
    aux = array[tupla[0]]
    array[tupla[0]] = array[tupla[1]]
    array[tupla[1]] = aux

def random_tuple(maximum):
    a = 0
    b = 0
    while a==b:
        a = random.randint(0, maximum)
        b = random.randint(0, maximum)

    return (a,b)    

def generate_neighbour(libraries, prob_temp):
    p = random.random() 
    if p < 0.2:
        #for n in noseke:
        swap(libraries, random_tuple(len(libraries)-1))
    else:
        #for n in noseke:
        selected = random.randint(0, len(libraries)-1)
        swap(libraries[selected].books, random_tuple(len(libraries[selected].books)-1))
        
    return libraries

def evaluate_solution(libraries, daysOfScanning):
    acum = 0
    signing = 1234
    ind_pointer = 0
    day_pointer = 0
    for i in range(daysOfScanning):
        if signing > 0:
            signing -= 1
        else:
            signing = libraries[ind_pointer].get_signup()
            acum += sum(libraries[ind_pointer].books[0:libraries[ind_pointer].get_perDay()*daysOfScanning-day_pointer])
            ind_pointer += 1
        day_pointer += 1

    return acum

def simulatedAnnealing(libraries, daysOfScanning):
    T_max = 1000.0
    T = 1000.0
    T_end = 0.01

    current = libraries
    best_found = libraries

    while T > T_end:
        new = generate_neighbour(libraries.copy(), 0)
            
        delta = evaluate_solution(new, daysOfScanning) - evaluate_solution(current, daysOfScanning)
        #print(delta)
        if delta >= 0:
            current = new.copy()
            best_found = current.copy()
        else:
            prob = math.exp(delta/T)
            #print(prob)
            if prob > random.random():
                current = new.copy()

        T = cooling(T)

    return best_found

assert_input()

file = open(sys.argv[1], "r")

numBooks, numLibraries, daysOfScanning = file.readline().split()
numBooks = int(numBooks)
numLibraries = int(numLibraries)
daysOfScanning = int(daysOfScanning)

scores = file.readline().split()
scores = list(map(int, scores))

libraries = []

for i_library in range(numLibraries):
    libNumBooks, signupDelay, shipCapacity = file.readline().split()
    libNumBooks = int(libNumBooks)
    signupDelay = int(signupDelay)
    shipCapacity = int(shipCapacity)
    books = file.readline().split()
    books = list(map(int, books))
    
    # DEBUG
    #print("numbooks:", libNumBooks)
    #print("signup:", signupDelay)
    #print("capacity:", shipCapacity)
    #print("books:", books)
    
    libraries.append(Library(i_library, books, signupDelay, shipCapacity))

shuffle_all(libraries)
best_solution = simulatedAnnealing(libraries, daysOfScanning)
write_output(best_solution)

