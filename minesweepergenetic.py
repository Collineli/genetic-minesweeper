#sorry to anyone who has to work with this code, including myself
from random import sample, uniform, randint, seed

#direction map used for gen_board function
direction_map = [
    (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
    ]

#this function returns list of mines' indexes. For example indexes of cells go like this (on 4x2 board)
#0, 1, 2, 3
#4, 5, 6, 7
def gen_mines(w, h, m):
    return sample(range(w*h), m)

def gen_board(w, h, mines): #mines - list of mines' indexes. likely inefficient function
    board = [x[:] for x in [[0]*w]*h] #initialize a 2D list of 0's
                                      #alternatively [[0]*w for y in range(h)]
    while mines:
        mine = mines.pop()
        y = mine//w
        x = mine%w
        board[y][x] = 'm'
        for direction in direction_map:
            a = y + direction[0]
            b = x + direction[1]
            if b<0 or a<0 or b>=w or a>=h:
                continue
            if board[a][b] != 'm':
                board[a][b] += 1
    return board

def count_numbers(board, number): #can be thought of as fitness function for our genetic algorithm.
                                  #because thats what we want to optimize
                                  #maybe could be made more pythonic 
    counter = 0
    for row in board:
        counter += row.count(number)
    return counter

def mutate(w, h, mines, p):
    """
    goes through every cell (index) and with probability p it will mutate it.
    (either add it to the list (i.e. empty cell becomes a mine)
    or remove it (mine becomes empty cell))
    """
    for i in range(w*h):
        if uniform(0, 1) <= p:
            #mutate:
            if i in mines:
                mines.remove(i)
            else:
                mines.append(i)
    return mines

def generate_population(size, w, h, N):
    """
    generates a population with given size of population, board's w(idth) and h(eight)
    N is used for the number that we want to optimize.
    Entity is stored as a tuple (list of indexes of mines, amount of N on the board).
    """
    population = []
    for _ in range(size):
        entity = gen_mines(w, h, randint(0, w*h))
        entity = (entity[:], count_numbers(gen_board(w, h, entity), N))
        population.append(entity)
        
    return population

def next_population(population, w, h, N):
    """
    based on given generation generate a new generation.

    maybe we could improve this function to improve its efficiency.
    currently it just takes top half of population, keeps it unmutated,
    and copies it and mutates the copy.
    """
    t = lambda entity: entity[1]
    population.sort(key=t, reverse=True)
    upper_half = population[:len(population)//2]
    mutated_half = []
    for entity in upper_half:
        new_entity = mutate(w, h, entity[0][:], 0.1) #0.1 as p seems to be pretty good in this config.
        new_entity = (new_entity[:], count_numbers(gen_board(w, h, new_entity), N))
        mutated_half.append(new_entity)
    return upper_half+mutated_half


#next 2 functions are me being lazy.
#theyre almost the same
#first one starts the main part of genetic algorithm from scratch
#i.e. it generate a new random population
#the second one can be used as function that will let you continue on old generation
def new_generations(n, w, h, num):
    generation = generate_population(100, w, h, num)
    for _ in range(n):
        generation = next_population(generation, w, h, num)
    return generation

def generations(n, w, h, num, generation):
    for _ in range(n):
        generation = next_population(generation, w, h, num)
    return generation

def mines_into_hex(w, h, mines):
    """
    this function is used to export the board into https://mzrg.com/js/mine/make_board.html
    """
    out = f'{hex(w)[2:].zfill(2)} {hex(h)[2:].zfill(2)} '

    #mines count
    count = len(mines)
    count = hex(count)[2:].zfill(4)
    out += f'{count[0:2]} {count[2:]}'

    #convert every mine to the mzrg.com format
    for mine in mines:
        my_x = mine%w
        my_y = mine//w

        a = hex(my_x)[2:].zfill(2)
        b = hex(my_y)[2:].zfill(2)

        out += f' {a} {b}'
        
    return out
