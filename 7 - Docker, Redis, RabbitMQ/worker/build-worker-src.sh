# Install prerequisites
apt-get update
export DEBIAN_FRONTEND=noninteractive 
apt-get install -y libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
apt-get install -y liblog4cplus-dev libcurl3-dev

# Clone the latest code from GitHub
cd /srv
git clone https://github.com/openalpr/openalpr.git

# Setup the build directory
cd /srv/openalpr/src
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
make -j8
make install

apt-get install -y python3 python3-pika python3-pillow python3-openalpr python3-redis