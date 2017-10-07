{% include 'elliptic.pxd' %}

cdef class MOABCore:
    cdef Core* inst

{% block content %}{% endblock %}
