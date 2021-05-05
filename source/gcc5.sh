# Install required libraries
sudo yum install libmpc-devel mpfr-devel gmp-devel

# Gather source code
export GCC_VERSION=5.5.0
cd /tmp
curl -o "gcc-${GCC_VERSION}.tar.gz" \
  https://ftp.gnu.org/gnu/gcc/gcc-${GCC_VERSION}/gcc-    ${GCC_VERSION}.tar.gz
tar xvzf "gcc-${GCC_VERSION}.tar.gz"
cd gcc-${GCC_VERSION}

# Configure and compile
./configure --with-system-zlib --disable-multilib --enable-languages=c,c++
make -j 8

# Install
sudo make install
