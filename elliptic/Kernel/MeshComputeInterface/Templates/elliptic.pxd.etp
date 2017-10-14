from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string as std_string


cdef extern from 'moab/Types.hpp' namespace "moab":

    ctypedef enum EntitySetProperty:
        MESHSET_TRACK_OWNER = 0x01
        MESHSET_SET = 0x02
        MESHSET_ORDERED = 0x03

    cdef enum DataType:
        MB_TYPE_OPAQUE   = 0
        MB_TYPE_INTEGER  = 1
        MB_TYPE_DOUBLE   = 2
        MB_TYPE_BIT      = 3
        MB_TYPE_HANDLE   = 4
        MB_MAX_DATA_TYPE = 4

    cdef enum TagType:
        MB_TAG_BIT
        MB_TAG_SPARSE
        MB_TAG_DENSE
        MB_TAG_MESH
        MB_TAG_BYTES
        MB_TAG_VARLEN
        MB_TAG_CREAT
        MB_TAG_EXCL
        MB_TAG_STORE
        MB_TAG_ANY
        MB_TAG_NOOPQ
        MB_TAG_DFTOK

    cdef cppclass TagInfo:
        pass

    ctypedef TagInfo* Tag;


cdef extern from "moab/Types.hpp" namespace "moab":

    cdef enum ErrorCode:
        MB_SUCCESS
        MB_INDEX_OUT_OF_RANGE
        MB_TYPE_OUT_OF_RANGE
        MB_MEMORY_ALLOCATION_FAILED
        MB_ENTITY_NOT_FOUND
        MB_MULTIPLE_ENTITIES_FOUND
        MB_TAG_NOT_FOUND
        MB_FILE_DOES_NOT_EXIST
        MB_FILE_WRITE_ERROR
        MB_NOT_IMPLEMENTED
        MB_ALREADY_ALLOCATED
        MB_VARIABLE_DATA_LENGTH
        MB_INVALID_SIZE
        MB_UNSUPPORTED_OPERATION
        MB_UNHANDLED_OPTION
        MB_STRUCTURED_MESH
        MB_FAILURE

cdef extern from "moab/EntityType.hpp" namespace "moab":

    ctypedef enum EntityType:
        MBVERTEX = 0
        MBEDGE
        MBTRI
        MBQUAD
        MBPOLYGON
        MBTET
        MBPYRAMID
        MBPRISM
        MBKNIFE
        MBHEX
        MBPOLYHEDRON
        MBENTITYSET
        MBMAXTYPE


cdef extern from "moab/EntityHandle.hpp" namespace "moab":

    ctypedef long EntityID
    ctypedef unsigned long EntityHandle

cdef extern from "moab/Range.hpp" namespace "moab":

    Range intersect(Range&, Range&)
    Range subtract(Range&, Range&)
    Range unite(Range&, Range&)

    cdef cppclass Range:
        Range()
        Range(EntityHandle val1, EntityHandle val2)

        size_t size()
        size_t psize()
        bint empty()
        void clear()
        bool all_of_type(EntityType t)
        bool all_of_dimension(int dimension)
        unsigned num_of_type( EntityType type )
        unsigned num_of_dimension( int dim )
        void print_ "print" ()
        void insert(EntityHandle val)
        void erase(EntityHandle val)
        void merge(Range& range)
        EntityHandle pop_front()
        EntityHandle pop_back()

        EntityHandle operator[](EntityID index)


cdef extern from "moab/Interface.hpp" namespace "moab":

    cdef cppclass Interface:
        Interface()


cdef extern from "moab/MeshTopoUtil.hpp" namespace "moab":

    cdef cppclass MeshTopoUtil:
        MeshTopoUtil(Interface *impl)

        ErrorCode construct_aentities(const Range &vertices)
        ErrorCode get_bridge_adjacencies(Range &from_entities,
                                         int bridge_dim,
                                         int to_dim,
                                         Range &to_ents,
                                         int num_layers)
        ErrorCode get_bridge_adjacencies(const EntityHandle from_entity,
                                         const int bridge_dim,
                                         const int to_dim,
                                         Range &to_adjs)
        ErrorCode get_average_position(Range& entities,
                                       double *avg_position)
        ErrorCode get_average_position(const EntityHandle *entities,
                                       const int num_entities,
                                       double * avg_position)


cdef extern from "moab/Core.hpp" namespace "moab":

    cdef cppclass Core:
        # Constructors
        Core()

        # member functions
        float impl_version()
        float impl_version(std_string *version_string)

        ErrorCode tag_get_handle(const char* name,
                                 Tag & tag_handle)

        ErrorCode tag_set_data(Tag& tag,
                                const EntityHandle* entity_handles,
                                int num_entities,
                                const void * data)

        ErrorCode write_file(const char *file_name)
        ErrorCode write_file(const char *file_name, const char *file_type)
        ErrorCode write_file(const char *file_name, const char *file_type,
                             const char *options)
        ErrorCode write_file(const char *file_name, const char *file_type,
                             const char *options, const EntityHandle *output_sets)
        ErrorCode write_file(const char *file_name, const char *file_type,
                             const char *options, const EntityHandle *output_sets,
                             int num_output_sets)
        #ErrorCode write_file(const char *file_name, const char *file_type,
        #                     const char *options, const EntityHandle *output_sets,
        #                     int num_output_sets, const Tag *tag_list)
        #ErrorCode write_file(const char *file_name, const char *file_type,
        #                     const char *options, const EntityHandle *output_sets,
        #                     int num_output_sets, const Tag *tag_list,
        #                     int num_tags)

        ErrorCode load_file(const char *file_name)
        ErrorCode load_file(const char *file_name, const EntityHandle* file_set)
        ErrorCode load_file(const char *file_name, const EntityHandle* file_set,
                            const char *options)
        ErrorCode load_file(const char *file_name, const EntityHandle* file_set,
                            const char *options, const char *set_tag_names)
        ErrorCode load_file(const char *file_name, const EntityHandle* file_set,
                            const char *options, const char *set_tag_names,
                            const char *set_tag_values)
        ErrorCode load_file(const char *file_name, const EntityHandle* file_set,
                            const char *options, const char *set_tag_names,
                            const char *set_tag_values, int num_set_tag_values)

        ErrorCode create_meshset(const unsigned int options, EntityHandle &ms_handle)
        ErrorCode create_meshset(const unsigned int options, EntityHandle &ms_handle, int start_id)

        ErrorCode add_entities(EntityHandle meshset, const EntityHandle *entities, int num_entities)
        ErrorCode add_entities(EntityHandle meshset, const Range &entities)

        ErrorCode create_vertices(const double *coordinates, const int nverts,
                                  Range &entity_handles)

        ErrorCode create_element(const EntityType type, const EntityHandle *connectivity,
                                 const int num_nodes, EntityHandle &element_handle)

        ErrorCode get_connectivity(const EntityHandle *entity_handles,
                                   const int num_handles,
                                   vector[EntityHandle] & connectivity)
        ErrorCode get_connectivity(const EntityHandle *entity_handles,
                                   const int num_handles,
                                   vector[EntityHandle] & connectivity,
                                   bool corners_only)
        ErrorCode get_connectivity(const EntityHandle *entity_handles,
                                   const int num_handles,
                                   vector[EntityHandle] & connectivity,
                                   bool corners_only,
                                   vector[int] * offsets)

        ErrorCode get_adjacencies(const EntityHandle *from_entities,
                                  const int num_entities,
                                  const int to_dimension,
                                  const bool create_if_missing,
                                  Range &adj_entities,
                                  const int operation_type = 0)
        ErrorCode get_adjacencies(const Range &from_entities,
                                  const int to_dimension,
                                  const bool create_if_missing,
                                  Range &adj_entities,
                                  const int operation_type = 0)
        EntityType type_from_handle(const EntityHandle handle)
        ErrorCode get_child_meshsets(EntityHandle meshset,
                                     Range &children,
                                     const int num_hops)
        ErrorCode get_parent_meshsets(EntityHandle meshset,
                                     Range &parents,
                                     const int num_hops)
        ErrorCode add_parent_meshset(EntityHandle child_meshset,
                                    const EntityHandle parent_meshset)
        ErrorCode add_child_meshset(EntityHandle parent_meshset,
                                    const EntityHandle child_meshset)
        ErrorCode add_parent_child(EntityHandle parent,
                                   EntityHandle child)
        ErrorCode get_coords(const EntityHandle* entity_handles,
                             const int num_entities,
                             double* coords)
        ErrorCode get_coords(const Range& entity_handles,
                             double* coords)
        ErrorCode set_coords(const EntityHandle* entity_handles,
                             const int num_entities,
                             const double* coords)
        ErrorCode set_coords(const Range& entity_handles,
                             const double* coords)
        ErrorCode get_entities_by_type(const EntityHandle meshset,
                                       const EntityType typ,
                                       vector[EntityHandle]& entities,
                                       const bool recursive)
        ErrorCode get_entities_by_type(const EntityHandle meshset,
                                       const EntityType typ,
                                       Range& entities,
                                       const bool recursive)

        ErrorCode get_entities_by_handle(const EntityHandle meshset,
                                         Range& entities,
                                         const bool recursive)
        ErrorCode get_entities_by_dimension(const EntityHandle meshset,
                                            const int dimension,
                                            Range& entities,
                                            const bool recursive)
        ErrorCode remove_entities(EntityHandle meshset,
                                  const EntityHandle* entities,
                                  const int num_entities)
        ErrorCode remove_entities(EntityHandle meshset,
                                  Range& entities)
        ErrorCode delete_entities(Range& entities)
        ErrorCode delete_entities(const EntityHandle* entities,
                                  const int num_entities)
        ErrorCode delete_mesh()


cdef extern from "moab/HomXform.hpp" namespace "moab":

     cdef cppclass HomCoord:
         #Constructors
         HomCoord()
         HomCoord(const HomCoord&)
         HomCoord(const int*, const int)
         HomCoord(const int, const int, const int, const int)
         HomCoord(const int, const int, const int)

         #Member functions
         const int* hom_coord()
         int& operator[](int)
         int i()
         int j()
         int k()
         int h()
         void set(const int coords[])
         void set(const int i, const int j, const int k, const int h)

         int length_squared()
         int length()
         void normalize()

         #operators
         HomCoord operator+(const HomCoord&) const
         HomCoord operator-(const HomCoord&) const
         bool operator==(const HomCoord&) const


cdef extern from "moab/ScdInterface.hpp" namespace "moab":

    cdef cppclass ScdParData:
        #Constructor
        ScdParData()

    cdef cppclass ScdInterface:
        #Constructor
        ScdInterface(Interface*, bint)

        #structured mesh creation
        ErrorCode construct_box(HomCoord low,
                                 HomCoord high,
                                const double * const coords,
                                unsigned int num_coords,
                                ScdBox *& new_box,
                                int * const lperiodic,
                                ScdParData * const par_data,
                                bool assign_global_ids,
                                int resolve_shared_ents)
        #Member functions
        ErrorCode find_boxes(Range &boxes)

    cdef cppclass ScdBox:
        HomCoord box_min()
        HomCoord box_max()
        HomCoord box_size()
        int num_vertices()
        int num_elements()
        EntityHandle start_vertex()
        EntityHandle start_element()
        EntityHandle get_vertex(int i, int j, int k)
        EntityHandle get_vertex(HomCoord& ijk)
        EntityHandle get_element(int i, int j, int k)
        EntityHandle get_element(HomCoord& ijk)
        ErrorCode get_params(EntityHandle ent, int &i, int &j, int &k)
        bool contains(int i, int j, int k)


cdef extern from "moab/Skinner.hpp" namespace "moab":

    cdef cppclass Skinner:
        #Constructor
        Skinner(Interface*)

        # Compute the geometric skin
        ErrorCode find_geometric_skin (const EntityHandle meshset, Range &forward_target_entities)

        # 	get skin entities of prescribed dimension
        #   will accept entities all of one dimension and return entities of n-1 dimension;
        #   NOTE: get_vertices argument controls whether vertices or entities of n-1 dimension are returned,
        #   and only one of these is allowed (i.e. this function returns only vertices or
        #   (n-1)-dimensional entities, but not both)
        # Defaults: *output_reverse_handles=0, create_vert_elem_adjs=false, create_skin_elements=true, look_for_scd=false
        ErrorCode 	find_skin (const EntityHandle meshset, const Range &entities, bool get_vertices,
                                Range &output_handles, Range *output_reverse_handles, bool create_vert_elem_adjs,
                                bool create_skin_elements, bool look_for_scd)
