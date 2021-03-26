
import random

def read_data(filename):
    harta = []

    with open(filename, "r") as f:

        nr_noduri = int(f.readline().strip())

        for i in range(0, nr_noduri):

            linie = []

            buffer = f.readline().strip().split(",")
            #  print(buffer)

            for el in buffer:
                linie.append(int(el))

            harta.append(linie)

        source = int(f.readline().strip())
        destination = int(f.readline().strip())

    return nr_noduri, harta, source, destination


def NNA(harta):
    vizitat = []

    for i in range(0, len(harta)):
        vizitat.append(0)

    nod_curent = 0

    vizitat[0] = 1

    counter = 1

    solution = [0]
    the_length = 0

    while counter < len(harta):

        best_length = 100000000000
        nod_selectat = -1

        for i in range(0, len(harta)):
            if vizitat[i] == 0 and harta[nod_curent][i] < best_length:
                best_length = harta[nod_curent][i]
                nod_selectat = i

        vizitat[nod_selectat] = 1

        solution.append(nod_selectat)
        the_length = the_length + best_length

        nod_curent = nod_selectat

        counter += 1

    return solution


def NNA_source_destination(harta, source, destination):
    vizitat = []

    for i in range(0, len(harta)):
        vizitat.append(0)

    nod_curent = source-1

    vizitat[source-1] = 1

    counter = 1

    solution = [source-1]
    the_length = 0

    destination_found = False

    while not destination_found:

        best_length = 10000000000
        nod_selectat = -1

        for i in range(0, len(harta)):
            if vizitat[i] == 0 and harta[nod_curent][i] < best_length:
                best_length = harta[nod_curent][i]
                nod_selectat = i

        vizitat[nod_selectat] = 1

        solution.append(nod_selectat)
        the_length = the_length + best_length

        nod_curent = nod_selectat

        if nod_curent == destination-1:
            destination_found = True

        counter+=1


    return solution

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
    solution = NNA(harta)
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
    solution = NNA_source_destination(harta,source,destination)
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


    print(nr_noduri)

    my_hill_climbing(harta)

#    print(nr_noduri)

#  my_hill_climbing_source_destination(harta, source, destination)

TSP()
