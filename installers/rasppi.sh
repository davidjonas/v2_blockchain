#!/bin/bash

echo "========== Installing Ethereum Blockchain and V2_Blockchain configuration =========="
cd $HOME
echo "Getting V2_Blockchain tools"
sudo apt-get -y install git
git clone https://github.com/davidjonas/v2_blockchain.git blockchain
cd blockchain
echo "installing ethereum-go..."
wget https://build.ethdev.com/builds/ARM%20Go%20develop%20branch/geth-ARM-latest.tar.bz2
tar -xf geth-ARM-latest.tar.bz2
rm geth-ARM-latest.tar.bz2
echo "Adding to the PATH variable..."
export PATH=$PATH:$HOME/blockchain
echo "export PATH=\$PATH:\$HOME/blockchain" >> ~/.bashrc
echo "installing Nodejs tools for GPIO and Ethereum..."
sudo apt-get -y install solc nodejs npm
mkdir nodejs
cd nodejs
npm install web3 onoff gpio-stream
echo "installing python tools"
pip install ethereum-ipc-client web3
