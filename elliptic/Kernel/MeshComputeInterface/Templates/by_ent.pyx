cimport elliptic

cdef class MOABCore:
    cdef elliptic.Core* inst


def callme(pymb):
    cdef elliptic.Core* mb = (<MOABCore>pymb).inst

    #cdef elliptic.EntityHandle ent
    cdef elliptic.Range ents
    cdef elliptic.Tag data_tag = NULL
    cdef elliptic.EntityHandle ent_array[1]
    cdef double vals_array[1]

    mb.tag_get_handle("cydata", data_tag)
    mb.get_entities_by_dimension(0, 2, ents, False)

    cdef unsigned int i = 0
    for i in range(0, ents.size()):
        ent_array[0] = ents[i]
        vals_array[0] = 1.0
        mb.tag_set_data(data_tag, ent_array, 1, vals_array)

    #mb.write_file("arquivo.vtk")

cdef elliptic.EntityHandle ent = 100
print ent

#cdef EntityHandle ent
#
#for ent in {{ ents }}:
#    {% for compute_node in compute_nodes %}
#    {{ compute_node }}
#    {% endfor %}
#    print(ent)
