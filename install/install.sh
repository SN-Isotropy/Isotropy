#!/bin/bash -xe
if [[ $# -gt 1 ]]
then
    echo "Do not understand more than 1 command line argument, found "$#; exit 1
fi
if [[ $# -gt 0 ]]
then
    opt=$1
else
    opt='all'
fi
echo "install script started with arguments "$opt
if [ $opt == 'all' ]
then
    echo "Install everything from scratch"
    source ./install/setup_env.sh
    ./install/install_miniconda.sh
    ./install/conda_install_dep.sh
    ./install/pip_install_dep.sh
else
    echo "Install only dependencies"
    source ./install/setup_env.sh
    ./install/conda_install_dep.sh
    ./install/pip_install_dep.sh
fi
