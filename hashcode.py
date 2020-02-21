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
        print(*books)
        #for book in books:
        #    print(book.get_id(), end=' ')
        #print()

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

def copy(sourceLibs):
    destLibs = [None] * len(sourceLibs)
    for i in range(len(sourceLibs)):
        destLibs[i] = Library(sourceLibs[i].num, sourceLibs[i].books.copy(), sourceLibs[i].signup, sourceLibs[i].perDay)
    return destLibs

def shuffle_all(libraries):
    random.shuffle(libraries)
    for library in libraries:
        random.shuffle(library.books)

def cooling(T):
    return 0.9*T

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
    for i in range(20):
        swap(libraries, random_tuple(len(libraries)-1))
    #else:
        #for n in noseke:
        selected = random.randint(0, len(libraries)-1)
        swap(libraries[selected].books, random_tuple(len(libraries[selected].books)-1))
        
    return libraries

def evaluate_solution(libraries, daysOfScanning, bookScores):
    score = 0
    day = 0
    scannedBooks = [False] * len(bookScores)
    
    for library in libraries:
        signing = library.get_signup()
        books = library.get_books()
        
        maxscan = library.get_perDay()*(daysOfScanning-day-signing)
        if maxscan > len(books):
            maxscan = len(books)
        
        acum = 0
        for i in range(maxscan):
            if scannedBooks[books[i]] == False:
                acum += bookScores[books[i]]
                scannedBooks[books[i]] = True
            else:
                if maxscan < len(books): maxscan += 1
        
        score += acum
        day += signing

    return score

def simulatedAnnealing(libraries, daysOfScanning, bookScores):
    T_max = 1000.0
    T = 1000.0
    T_end = 0.01
    
    current = []
    best_found = []
    current = copy(libraries)
    best_found = copy(libraries)
    
    #current = libraries.copy()
    #best_found = libraries.copy()

    while T > T_end:
        new = generate_neighbour(copy(current), 0)
                
        #print_libraries(new)
        #print()
        #print_libraries(current)
        #print("#",evaluate_solution(new, daysOfScanning, bookScores), evaluate_solution(current, daysOfScanning, bookScores))
        #print("-------")
        
        delta = float(evaluate_solution(new, daysOfScanning, bookScores) - evaluate_solution(current, daysOfScanning, bookScores))
        
        if delta > 0:
            current = copy(new)
            best_found = copy(current)
            #current = new.copy()
            #best_found = current.copy()
        else:
            prob = math.exp(delta/T)
            #print(delta, prob)
            if prob > random.random():
                current = copy(new)
                #current = new.copy()

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
best_solution = simulatedAnnealing(libraries, daysOfScanning, scores)
print_libraries(best_solution)

