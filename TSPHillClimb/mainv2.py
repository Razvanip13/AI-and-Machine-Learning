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

    the_length = the_length + harta[nod_curent][0]

    show_string = ""

    for i in range(0, len(solution)):
        show_string = show_string + str(solution[i] + 1) + " "

    print(show_string)
    print(the_length)


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



    show_string = ""

    for i in range(0, len(solution)):
        show_string = show_string + str(solution[i] + 1) + " "


    print(counter)
    print(show_string)
    print(the_length)


def TSP():
    nr_noduri, harta, source, destination = read_data("test4.txt")

    print(nr_noduri)

    NNA(harta)

    NNA_source_destination(harta,source,destination)


TSP()
