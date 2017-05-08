# Authors:
# Guilherme Caminha <gpkc@cin.ufpe.br>

FROM phusion/baseimage
MAINTAINER Guilherme Caminha <gpkc@cin.ufpe.br>

ENV HOME /home/scientific

ENV MOAB_DIR /usr
ENV VISIT_DIR /opt/visit
ENV MPI_HOME /usr
ENV PYTHONPATH /usr/lib/python2.7/site-packages

RUN set -x \
    && apt-get update \
    && apt-get -qy install python-software-properties \
        wget pkg-config git libopenblas-dev liblapack-dev \
        make cmake autoconf automake libtool python \
        clang gcc g++ gfortran \
        libhdf5-mpich-dev libnetcdf-c++4 \
        libeigen3-dev libmetis-dev doxygen \
        liboce-foundation-dev liboce-modeling-dev liboce-ocaf-dev liboce-visualization-dev oce-draw \
        netgen libnglib-dev  \
        python-setuptools python-numpy cython python-nose \
        build-essential bzip2 tar m4 file swig \
    && apt-get clean

CMD ["/sbin/my_init"]


# Install mpi4py
WORKDIR $HOME
RUN cd $HOME \
    && git clone https://bitbucket.org/mpi4py/mpi4py \
    && cd $HOME/mpi4py \
    && python setup.py build \
    && python setup.py install \
    && cd $HOME \
    && rm -rf mpi4py


# Install MOAB
WORKDIR $HOME
RUN cd $HOME \
    && git clone https://bitbucket.org/fathomteam/moab.git \
    && cd $HOME/moab \
    && git checkout pshriwise/pymoab \
    && autoreconf -fi \
    && mkdir build \
    && cd $HOME/moab/build \
    && ../configure \
            --prefix=$MOAB_DIR \
            --with-mpi=/usr \
            --with-hdf5=/usr/lib/x86_64-linux-gnu/hdf5/mpich \
            --with-netcdf=/usr \
            --with-metis=/usr \
            --enable-optimize \
            --enable-debug \
            --enable-tools \
            --enable-pymoab \
            --enable-shared \
            CFLAGS='-O2 -fPIC -DPIC' \
            CXXFLAGS='-O2 -fPIC -DPIC' \
            FCFLAGS='-O2 -fPIC' \
            FFLAGS='-O2 -fPIC' \
    && make -j 10 \
    && make install \
    && cd $HOME/moab/build/pymoab \
    && python setup.py build \
    && python setup.py install \
    && cd $HOME \
    && rm -rf moab \
    && echo "export MOAB_DIR=$MOAB_DIR" >> $HOME/.bashrc \
    && echo "export PATH=$PATH:$MOAB_DIR/bin" >> $HOME/.bashrc \
    && echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MOAB_DIR/lib" >> $HOME/.bashrc



# Install Trilinos
RUN cd $HOME \
    && wget http://www.cmake.org/files/v3.2/cmake-3.2.2.tar.gz \
    && tar xzvf cmake-3.2.2.tar.gz \
    && cd $HOME/cmake-3.2.2 \
    && ./configure --prefix=/usr/local/cmake \
    && make -j 14 && make install \
    && cd $HOME \
    && rm -rf cmake-3.2.2 && rm -f cmake-3.2.2.tar.gz \
    && wget http://trilinos.csbsju.edu/download/files/trilinos-11.14.2-Source.tar.bz2 \
    && tar xjvf trilinos-11.14.2-Source.tar.bz2 \
    && mkdir trilinos-11.14.2-Source/build \
    && cd $HOME/trilinos-11.14.2-Source/build/ \
    && /usr/local/cmake/bin/cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr \
          \
          -D MPI_BASE_DIR:PATH=/usr \
          \
          -D CMAKE_BUILD_TYPE:STRING=Release \
          -D CMAKE_Fortran_COMPILER:FILEPATH=/usr/bin/mpif90 \
          -D BUILD_SHARED_LIBS:BOOL=ON \
          -D Trilinos_WARNINGS_AS_ERRORS_FLAGS:STRING="" \
          \
          -D Trilinos_ENABLE_ALL_PACKAGES:BOOL=OFF \
          -D Trilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF \
          -D Trilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=OFF \
          -D Trilinos_ENABLE_Teuchos:BOOL=ON \
          -D Trilinos_ENABLE_Epetra:BOOL=ON \
          -D Trilinos_ENABLE_AztecOO:BOOL=ON \
          -D Trilinos_ENABLE_Amesos:BOOL=ON \
          -D Trilinos_ENABLE_PyTrilinos:BOOL=ON \
          \
          -D PyTrilinos_DISABLE_STRONG_WARN:BOOL=OFF\
          -D PyTrilinos_DOCSTRINGS:BOOL=ON \
          -D PyTrilinos_ENABLE_EXAMPLES:BOOL=OFF \
          -D PyTrilinos_ENABLE_TESTS:BOOL=OFF\
          \
          -D Trilinos_ENABLE_EXAMPLES:BOOL=OFF \
          -D Trilinos_ENABLE_TESTS:BOOL=OFF \
          \
          -D TPL_ENABLE_MATLAB:BOOL=OFF \
          -D TPL_ENABLE_Matio:BOOL=OFF \
          -D TPL_ENABLE_MPI:BOOL=ON \
          -D TPL_ENABLE_BLAS:BOOL=ON \
          -D TPL_ENABLE_LAPACK:BOOL=ON \
          -D TPL_ENABLE_QT:BOOL=OFF \
          -D TPL_ENABLE_X11:BOOL=OFF \
          -D TPL_ENABLE_MPI4PY:BOOL=ON \
          \
          -D CMAKE_VERBOSE_MAKEFILE:BOOL=OFF \
          -D Trilinos_VERBOSE_CONFIGURE:BOOL=OFF \
          .. \
    && make -j 14 && make install \
    && cd $HOME \
    && rm -rf trilinos-11.14.2-Source trilinos-11.14.2-Source.tar.bz2
