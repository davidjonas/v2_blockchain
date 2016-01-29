echo "========== Installing Ethereum Blockchain and V2_Blockchain configuration =========="
echo "Installing homebrew"
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo "Installing git"
brew install git

cd $HOME
echo "Getting V2_Blockchain tools"
git clone https://github.com/davidjonas/v2_blockchain.git blockchain
cd blockchain

echo "Adding to the PATH variable..."
export PATH=$PATH:$HOME/blockchain
echo "export PATH=\$PATH:\$HOME/blockchain" >> ~/.bashrc



echo "Installing ccp-ethereum and solidity compiler for the editor"
brew tap ethereum/ethereum
brew install ethereum
brew install cpp-ethereum
brew linkapps cpp-ethereum
