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

def write_output(dicc, best_solution):
    
    print(len(dicc))
    
    for ilibrary in best_solution:
        library = dicc[ilibrary]
        print(ilibrary,len(library))
        print(*library)
    

class Library:
    def __init__(self, books, signup, perDay):
        self.books = books
        self.signup = signup
        self.perDay = perDay
    def get_books(self):
        return self.books
    def get_signup(self):
        return self.signup
    def get_perDay(self):
        return self.perDay


def generate_library(libraries, numBooks, numLibraries, daysOfScanning):
    dicc = {}
    i=0
    for l in libraries:
        dicc[i] = l.get_books()
        i += 1

    return dicc

def generate_random(libraries, numBooks, numLibraries, daysOfScanning):
    individual = []
    for i in range(numLibraries):
        individual.append(i)

    return individual

def cooling(T):
    return 0.90*T

def generate_neighbour(individual, dicc):
    p = random.random() 
    if p >= 0.2:
        a = 0
        b = 0
        while a==b:
            a = random.randint(0, len(individual)-1)
            b = random.randint(0, len(individual)-1)
        aux_l = individual[a]
        individual[a] = individual[b]
        individual[b] = aux_l

    else:
        selected = random.randint(0, len(individual)-1)
        a = 0
        b = 0
        while a==b:
            a = random.randint(0, len(dicc[individual[selected]])-1)
            b = random.randint(0, len(dicc[individual[selected]])-1)
        aux_b = dicc[individual[selected]][a]
        dicc[individual[selected]][a] = dicc[individual[selected]][b]
        dicc[individual[selected]][b] = aux_b


    return individual

def evaluate_solution(individual, daysOfScanning, dicc, libraries):
    acum = 0

    matrix = [[0] * daysOfScanning] * len(individual)

    signing = 1234
    ind_pointer = 0
    day_pointer = 0
    for i in range(daysOfScanning):
        if signing > 0:
            signing -= 1

        else:
            aux_books = dicc[individual[ind_pointer]]
            signing = libraries[individual[ind_pointer]].get_signup()
            acum += sum(aux_books[0:daysOfScanning-day_pointer])
            ind_pointer += 1
        day_pointer += 1

    #acum = sum(sum(matrix,[]))

    return acum

def simulatedAnnealing(_X, daysOfScanning, dicc, libraries):
    T = 1000.0
    T_end = 0.01

    current = _X
    best_found = _X

    while T > T_end:
        new = generate_neighbour(current.copy(), dicc)
            
        delta = evaluate_solution(new, daysOfScanning, dicc, libraries) - evaluate_solution(current, daysOfScanning, dicc, libraries)

        if delta >= 0:
            current = new.copy()
            best_found = current.copy()
        else:
            prob = math.exp(delta/T)
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
    
    #print("numbooks:", libNumBooks)
    #print("signup:", signupDelay)
    #print("capacity:", shipCapacity)
    #print("books:", books)
    
    libraries.append(Library(books, signupDelay, shipCapacity))


dicc = generate_library(libraries, numBooks, numLibraries, daysOfScanning)
_X = generate_random(libraries, numBooks, numLibraries, daysOfScanning)
best_solution = simulatedAnnealing(_X, daysOfScanning, dicc, libraries)

#print("Best score: "+str(evaluate_solution(best_solution, items, portions)))

write_output(dicc, best_solution)

#file2 = open("solution.out", "w")
#file2.write(str(sum(best_solution)))
#file2.write("\n")
#types_of_piz
