{% include 'elliptic.pxd' %}

cdef class MOABCore:
    cdef Core* inst

{{ child }}
