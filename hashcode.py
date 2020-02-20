import math
import random

def write_output(libraries, orderedlibs):
    
    print(len(libraries))
    
    for ilibrary in orderedlibs:
        library = libraries[ilibrary]
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
    return 0.99*T

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
            for j in range(len(matrix)):
                acum += matrix[j][day_pointer]
            signing -= 1

        else:
            for j in range(len(matrix)):
                acum += matrix[j][day_pointer]

            aux_books = dicc[individual[ind_pointer]]
            signing = libraries[individual[ind_pointer]].get_signup()
            matrix[ind_pointer][day_pointer:daysOfScanning-1] = aux_books[0:daysOfScanning-day_pointer]
            ind_pointer += 1
        day_pointer += 1


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

file = open("f_libraries_of_the_world.txt", "r")
numBooks, numLibraries, daysOfScanning = file.readline().split()
numBooks = int(numBooks)
numLibraries = int(numLibraries)
daysOfScanning = int(daysOfScanning)

scores = file.readline().split()
scores = list(map(int, scores))

aux_file = file.readlines()

libraries = []
i = 0
params_aux = []
for l in aux_file:
    if i==0:
        params_aux = l.split()
        i += 1
    elif i==1:
        aux = l.split()
        lib = Library(aux, params_aux[1], params_aux[2])
        libraries.append(lib)
        i = 0


dicc = generate_library(libraries, numBooks, numLibraries, daysOfScanning)
_X = generate_random(libraries, numBooks, numLibraries, daysOfScanning)
best_solution = simulatedAnnealing(_X, daysOfScanning, dicc, libraries)

#print("Best score: "+str(evaluate_solution(best_solution, items, portions)))

write_output(dicc, best_solution)

#file2 = open("solution.out", "w")
#file2.write(str(sum(best_solution)))
#file2.write("\n")
#types_of_piz
