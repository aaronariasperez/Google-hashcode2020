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
import copy

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

def print_libraries(libraries):
    
    print(len(libraries))
    
    for library in libraries:
        books = library.books
        print(library.get_id(),len(books))
        for book in books:
            print(book.get_id(), end=' ')
        print()

class Book:
    def __init__(self, num, value):
        self.num = num
        self.value = value
        self.scanned = False
    def get_id(self):
        return self.num
    def get_value(self):
        return self.value

class Library:
    def __init__(self, num, books, signup, perDay):
        self.num = num
        self.books = books
        self.signup = signup
        self.perDay = perDay
    def get_id(self):
        return self.num
    def get_books(self):
        return self.books
    def get_signup(self):
        return self.signup
    def get_perDay(self):
        return self.perDay

def shuffle_all(libraries):
    random.shuffle(libraries)
    for library in libraries:
        random.shuffle(library.books)

def cooling(T):
    return 0.1*T

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
    # balancear carga de swaps n_librerias vs. n_books
    #p = random.random() 
    #if p < 0.2:
        #for n in noseke:
        swap(libraries, random_tuple(len(libraries)-1))
    #else:
        #for n in noseke:
        selected = random.randint(0, len(libraries)-1)
        swap(libraries[selected].books, random_tuple(len(libraries[selected].books)-1))
        
        return libraries

def evaluate_solution(libraries, daysOfScanning):
    score = 0
    day = 0
    
    for library in libraries:
        signing = library.get_signup()
        books = copy.deepcopy(library.get_books())
        
        maxscan = library.get_perDay()*(daysOfScanning-day-signing)
        if maxscan > len(books):
            maxscan = len(books)
        
        #print("library:", library.get_id(), "maxscan:", maxscan)
        
        acum = 0
        for i in range(maxscan):
            if books[i].scanned == False:
                acum += books[i].get_value()
                #print("value:", library.books[i].get_value())
                books[i].scanned = True
            else:
                if maxscan < len(books): maxscan += 1
        
        score += acum
        day += signing

    return score

def simulatedAnnealing(libraries, daysOfScanning):
    T_max = 1000.0
    T = 1000.0
    T_end = 0.01

    current = libraries.copy()
    best_found = libraries.copy()

    while T > T_end:
        new = generate_neighbour(current.copy(), 0)
                
        #print_libraries(current)
        #print()
        #print_libraries(new)
        #print("-------")
        #print("#",evaluate_solution(new, daysOfScanning), evaluate_solution(current, daysOfScanning))
        
        delta = float(evaluate_solution(new, daysOfScanning) - evaluate_solution(current, daysOfScanning))
        
        if delta > 0:
            current = new.copy()
            best_found = current.copy()
        else:
            prob = math.exp(delta/T)
            print(delta, prob)
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

_libraries = []
_books = []
for ibook in range(numBooks):
    _books.append(Book(ibook, scores[ibook]))

for i_library in range(numLibraries):
    libNumBooks, signupDelay, shipCapacity = file.readline().split()
    libNumBooks = int(libNumBooks)
    signupDelay = int(signupDelay)
    shipCapacity = int(shipCapacity)
    bookids = file.readline().split()
    bookids = list(map(int, bookids))
    
    libbooks = []
    for bookid in bookids:
        libbooks.append(_books[bookid])
    
    # DEBUG
    #print("numbooks:", libNumBooks)
    #print("signup:", signupDelay)
    #print("capacity:", shipCapacity)
    #print("books:", books)
    
    _libraries.append(Library(i_library, libbooks, signupDelay, shipCapacity))

shuffle_all(_libraries)
best_solution = simulatedAnnealing(_libraries, daysOfScanning)
print_libraries(best_solution)

