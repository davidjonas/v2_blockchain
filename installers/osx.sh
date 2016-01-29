echo "========== Installing Ethereum Blockchain and V2_Blockchain configuration =========="
cd $HOME
echo "Getting V2_Blockchain tools"
sudo apt-get -y install git
git clone https://github.com/davidjonas/v2_blockchain.git blockchain
cd blockchain

sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo add-apt-repository -y ppa:ethereum/ethereum-dev
sudo apt-get update
sudo apt-get install -y ethereum

echo "installing homebrew"

echo "Installing ccp-ethereum and solidity compiler for the editor"
brew install cpp-ethereum
brew linkapps cpp-ethereum
