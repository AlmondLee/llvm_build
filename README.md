apt -y install glibc-dev.i686 glibc-dev ncurses ncurses-dev zlib-dev bzip2-dev openssl-dev readline-dev sqlite-dev tk-dev gdbm-dev db4-dev libpcap-dev xz-dev texinfo bison flex python-dev libffi-dev graphviz-dev elfutils-libelf-dev libedit-dev libxml2-dev protobuf-dev gtext-dev doxygen swig

yum -y install glibc-devel.i686 glibc-devel ncurses ncurses-devel zlib-devel bzip2-devel openssl-devel readline-devel sqlite-devel tk-devel gdbm-devel    db4-devel libpcap-devel xz-devel texinfo bison flex python-devel libffi-devel graphviz-devel elfutils-libelf-devel libedit-devel libxml2-devel protobuf-devel gtext-devel doxygen swig
yum -y install yum-utils
yum-builddep -y llvm clang
pip install distribute


    export LLVM_VERSION="8.0.0"

    /sbin/ldconfig
    wget http://releases.llvm.org/$LLVM_VERSION/llvm-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/cfe-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/compiler-rt-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/libcxx-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/libcxxabi-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/libunwind-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/lld-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/lldb-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/openmp-$LLVM_VERSION.src.tar.xz
    wget http://releases.llvm.org/$LLVM_VERSION/polly-$LLVM_VERSION.src.tar.xz
//    wget http://releases.llvm.org/$LLVM_VERSION/clang-tools-extra-$LLVM_VERSION.src.tar.xz


    tar xf llvm-$LLVM_VERSION.src.tar.xz
    tar xf cfe-$LLVM_VERSION.src.tar.xz && mv cfe-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/tools/clang
    tar xf lld-$LLVM_VERSION.src.tar.xz && mv lld-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/tools/lld
    tar xf lldb-$LLVM_VERSION.src.tar.xz && mv lldb-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/tools/lldb
    tar xf polly-$LLVM_VERSION.src.tar.xz && mv polly-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/tools/polly
//    tar xf clang-tools-extra-$LLVM_VERSION.src.tar.xz && mv clang-tools-extra-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/tools/clang/tools/extra
    tar xf compiler-rt-$LLVM_VERSION.src.tar.xz && mv compiler-rt-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/projects/compiler-rt
    tar xf libcxx-$LLVM_VERSION.src.tar.xz && mv libcxx-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/projects/libcxx
    tar xf libcxxabi-$LLVM_VERSION.src.tar.xz && mv libcxxabi-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/projects/libcxxabi
    tar xf libunwind-$LLVM_VERSION.src.tar.xz && mv libunwind-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/projects/libunwind
    tar xf openmp-$LLVM_VERSION.src.tar.xz && mv openmp-$LLVM_VERSION.src/ llvm-$LLVM_VERSION.src/projects/openmp

    cd llvm-$LLVM_VERSION.src/
    mkdir llvm-build
    cd llvm-build/
    /sbin/ldconfig
    cmake .. -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=/usr/local/clang -DCMAKE_BUILD_TYPE=Release
    make -j8
    make install


    echo "/usr/local/clang/lib" > /etc/ld.so.conf.d/clang.conf
    echo "/usr/local/clang/libexec" > /etc/ld.so.conf.d/clanglibexec.conf
    /sbin/ldconfig

