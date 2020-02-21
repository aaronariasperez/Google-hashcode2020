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

def assertInput():
     if len(sys.argv) < 2:
        print("Script arguments are chungos. Usage: $ python3 script.py inputnamefile.txt")
        exit()
     if not os.path.exists(sys.argv[1]):
        print(sys.argv[1], "no existe ompare, no me la cuelas")
        exit()   
     if not os.path.isfile(sys.argv[1]):
        print(sys.argv[1], "está ma duro que zu puta madre... pa mi que ezo no es un fichero")
        exit()

def printOutput(libraries):
    print(len(libraries))
    for library in libraries:
        books = library.books
        print(library.getId(),len(books))
        print(*books)

class Library:
    def __init__(self, num, books, signup, perDay):
        self.num = num
        self.books = books
        self.signup = signup
        self.perDay = perDay
    def getId(self):
        return self.num
    def getBooks(self):
        return self.books
    def getSignup(self):
        return self.signup
    def getPerDay(self):
        return self.perDay

def copy(sourceLibs):
    destLibs = [None] * len(sourceLibs)
    for i in range(len(sourceLibs)):
        destLibs[i] = Library(sourceLibs[i].num, sourceLibs[i].books.copy(), sourceLibs[i].signup, sourceLibs[i].perDay)
    return destLibs

def shuffleAll(libraries):
    random.shuffle(libraries)
    for library in libraries:
        random.shuffle(library.books)

def cooling(T):
    return 0.9*T

def swap(array, tupla):
    aux = array[tupla[0]]
    array[tupla[0]] = array[tupla[1]]
    array[tupla[1]] = aux

def randomTuple(maximum):
    a = 0
    b = 0
    while a==b:
        a = random.randint(0, maximum)
        b = random.randint(0, maximum)

    return (a,b)    

def generateNeighbour(libraries, probTemp):
    # TODO: balancear carga de swaps n_librerias vs. n_books
    for i in range(20):
        swap(libraries, randomTuple(len(libraries)-1))
        selected = random.randint(0, len(libraries)-1)
        swap(libraries[selected].books, randomTuple(len(libraries[selected].books)-1))
    return libraries

def evaluateSolution(libraries, daysOfScanning, bookScores):
    score = 0
    day = 0
    scannedBooks = [False] * len(bookScores)
    
    for library in libraries:
        signing = library.getSignup()
        books = library.getBooks()
        
        maxscan = library.getPerDay()*(daysOfScanning-day-signing)
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
    bestFound = []
    current = copy(libraries)
    bestFound = copy(libraries)

    while T > T_end:
        new = generateNeighbour(copy(current), 0)
        
        delta = float(evaluateSolution(new, daysOfScanning, bookScores) - evaluateSolution(current, daysOfScanning, bookScores))
        
        if delta > 0:
            current = copy(new)
            bestFound = copy(current)
        else:
            prob = math.exp(delta/T)
            if prob > random.random():
                current = copy(new)

        T = cooling(T)

    return bestFound

# INICIO
assertInput()
file = open(sys.argv[1], "r")

numBooks, numLibraries, daysOfScanning = file.readline().split()
numBooks = int(numBooks)
numLibraries = int(numLibraries)
daysOfScanning = int(daysOfScanning)

scores = file.readline().split()
scores = list(map(int, scores))

libraries = []

for iLibrary in range(numLibraries):
    libNumBooks, signupDelay, shipCapacity = file.readline().split()
    libNumBooks = int(libNumBooks)
    signupDelay = int(signupDelay)
    shipCapacity = int(shipCapacity)
    books = file.readline().split()
    books = list(map(int, books))
    
    libraries.append(Library(iLibrary, books, signupDelay, shipCapacity))

shuffleAll(libraries)
bestSolution = simulatedAnnealing(libraries, daysOfScanning, scores)
printOutput(bestSolution)

