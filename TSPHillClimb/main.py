import random


def read_data(filename):
    harta = []

    with open(filename, "r") as f:

        nr_noduri = int(f.readline().strip())

        for i in range(0, nr_noduri):

            linie = []

            buffer = f.readline().strip().split(",")
           # print(buffer)

            for el in buffer:
                linie.append(int(el))

            harta.append(linie)

        source = int(f.readline().strip())
        destination = int(f.readline().strip())

    return nr_noduri, harta, source, destination


def randomStartPoint(harta, source=-1, destination=-1):
    start_solution = []

    if source == -1:

        vertices = list(range(0, len(harta)))

        for index in range(0, len(harta)):
            randomVertex = vertices[random.randint(0, len(vertices) - 1)]

            start_solution.append(randomVertex)

            vertices.remove(randomVertex)

        return start_solution

    else:

        vertices = list(range(0, len(harta)))

        for index in range(1, len(harta) - 1):

            randomVertex = vertices[random.randint(0, len(vertices) - 1)]

            while randomVertex == source or randomVertex == destination:
                vertices.remove(randomVertex)
                randomVertex = vertices[random.randint(0, len(vertices) - 1)]

            start_solution.append(randomVertex)

            vertices.remove(randomVertex)

        start_solution.insert(0, source)
        start_solution.append(destination)

        return start_solution


def find_neighbours(solution, source=-1):
    neighbours = []

    if source < 0:

        for i in range(0, len(solution)):

            for j in range(i + 1, len(solution)):
                copy = solution[:]

                aux = copy[i]
                copy[i] = copy[j]
                copy[j] = aux

                neighbours.append(copy)

        return neighbours

    else:

        for i in range(1, len(solution) - 1):

            for j in range(i + 1, len(solution) - 1):
                copy = solution[:]

                aux = copy[i]
                copy[i] = copy[j]
                copy[j] = aux

                neighbours.append(copy)

        return neighbours


def routeLength(harta, solution, source=-1):
    the_length = 0

    if source < 0:

        for index in range(0, len(solution)):
            the_length = the_length + harta[solution[index - 1]][solution[index]]

    else:

        for index in range(1, len(solution)):
            the_length = the_length + harta[solution[index - 1]][solution[index]]

    return the_length


def best_solution_in_vicinity(harta, neighbours, source=-1):



    if source < 0:

        best_candidate_length = routeLength(harta, neighbours[0])
        best_candidate = neighbours[0]

        for neighbour in neighbours:

            current_length = routeLength(harta, neighbour)

            if current_length < best_candidate_length:
                best_candidate_length = current_length
                best_candidate = neighbour

        return best_candidate, best_candidate_length

    else:

        best_candidate_length = routeLength(harta, neighbours[0],source)
        best_candidate = neighbours[0]

        for neighbour in neighbours:

            current_length = routeLength(harta, neighbour, source)

            if current_length < best_candidate_length:
                best_candidate_length = current_length
                best_candidate = neighbour

        return best_candidate, best_candidate_length


def my_hill_climbing(harta):
    solution = randomStartPoint(harta)
    solution_length = routeLength(harta, solution)
    neighbours = find_neighbours(solution)

    # print(neighbours)

    best_candidate, best_candidate_length = best_solution_in_vicinity(harta, neighbours)

    while best_candidate_length < solution_length:
        solution = best_candidate

        solution_length = best_candidate_length

        neighbours = find_neighbours(solution)

        # print(neighbours)

        best_candidate, best_candidate_length = best_solution_in_vicinity(harta, neighbours)

   # solution.append(solution[0])

    show_string = ""

    for i in range(0, len(solution)):
        solution[i] += 1
        show_string = show_string + str(solution[i]) + " "

    print(show_string)
    print(solution_length)


def my_hill_climbing_source_destination(harta, source, destination):
    solution = randomStartPoint(harta, source - 1, destination - 1)
    solution_length = routeLength(harta, solution, source - 1)
    neighbours = find_neighbours(solution,source-1)

    #print(neighbours)

    best_candidate, best_candidate_length = best_solution_in_vicinity(harta, neighbours,source-1)

    #print(best_candidate)

    while best_candidate_length < solution_length:
        solution = best_candidate

        solution_length = best_candidate_length

        neighbours = find_neighbours(solution,source-1)

        #print(neighbours)

        best_candidate, best_candidate_length = best_solution_in_vicinity(harta, neighbours,source-1)

    show_string = ""

    for i in range(0, len(solution)):
        solution[i] += 1
        show_string = show_string + str(solution[i]) + " "

    print(show_string)
    print(solution_length)


def TSP():
    nr_noduri, harta, source, destination = read_data("hard_tsp.txt")

    '''
    print(nr_noduri)

    for i in range(0, len(harta)):

        linie = ""

        for j in range(0, len(harta)):
            linie = linie + str(harta[i][j]) + " "

        print(linie)

    print(source)
    print(destination)
    '''

    print(nr_noduri)

    my_hill_climbing(harta)

    print(nr_noduri)

    my_hill_climbing_source_destination(harta, source, destination)


if __name__ == '__main__':
    TSP()
