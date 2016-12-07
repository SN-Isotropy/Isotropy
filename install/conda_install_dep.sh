#!/bin/bash -xe
export PATH="${store_dir}/miniconda/bin:$PATH"
#CHANNEL=${CHANNEL:-"http://conda.lsst.codes/sims"} # the URL to the conda channel where LSST conda packages reside
#conda config --add channels "$CHANNEL"
# CHANNEL=${CHANNEL:-"pandas"}
#conda config --add channels "$CHANNEL"
#CHANNEL=${CHANNEL:-"astropy"}
conda config --add channels pandas 
conda config --add channels astropy
conda config --add channels conda-forge
# conda create --yes -n AnalyzeSN python
# source activate AnalyzeSN
conda install -q --yes --file ./install/requirements.txt
conda list --explicit > spec-file.txtconda list --explicit > ./install/spec-file.txt;

