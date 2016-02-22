# v2_blockchain
Tools for exploring the potential of ethereum blockchain on the V2_Blockchain network.
These are helper scripts that deal with all the configuration and installation of all the tools necessary to run Ethereum nodes.
The project is all centralized on the v2bc application that is basically a wrapper on top of geth, the Go-language implementation of the Ethereum client.

# One-liner installers
Run these commands on the terminal to download and install all the tools necessary

## Raspberry pi
```shell
curl https://raw.githubusercontent.com/davidjonas/v2_blockchain/master/installers/rasppi.sh | sh
```

## Ubuntu
```shell
curl https://raw.githubusercontent.com/davidjonas/v2_blockchain/master/installers/ubuntu.sh | sh
```

## Mac OSX
```shell
curl https://raw.githubusercontent.com/davidjonas/v2_blockchain/master/installers/osx.sh | sh
```

# Usage:

### Help on all the options:
```shell
v2bc --help
```

### Creating a node and an account (multiple can be created and ran on the same machine):
```shell
v2bc -i NODENAME create
```

### Listing all the created nodes on this machine:
```shell
v2bc list
```

### Starting the node:
```shell
v2bc -i NODENAME start
```

### Or interactive mode:
```shell
v2bc -i NODENAME console
```

### Attaching a console to a running node:
```shell
v2bc -i NODENAME attach
```

### Starting the node and unlocking the account:
```shell
v2bc -i NODENAME console --unlock
```
(You will need to type the passphrase for the account as the first input when starting the console)
(This is necessary to submit contracts with the editor)

### Runing a miner:
```shell
v2bc -i NODENAME mine
```

### Getting the config string:
```shell
v2bc -i NODENAME configstring
```

This will print out all the configurations used for this node. Basically this string can be copy/pasted into the geth command to run that node. This might be useful when someone wants to run a node with some special configurations.

# Smart contract editor:
The smart contract editor needs to be ran on a node. The node needs to be running on the machine with the --unlock option or the coinbase user of that node needs to be unlocked in the console before submitting the contract. The editor creates a small HTTP server running on port 8888 to render the UI but the editor will only work locally.

### Starting the editor (On a new terminal):
```shell
v2bc -i NODENAME editor
```

The editor accepts solidity input and compiles it, sends it to the node and submits it to the network by sending a transaction on the blockchain. It will then wait for the contract to be mined, once it gets mined it will display the address of the new contract and generate/download a json file with the contract information. This file has the necessary information to call the contract. That would be the address (hash) of the contract and the ABI (Application Binary Interface)

### Running the contracts
Helpers for loading contract json files and calling functions are not yet implemented. They are pretty easy to do though through the console or by connecting to the node from nodejs, python, javascript or any other programing language through the RPC JSON protocol or the IPC socket offered by geth.
The installer also installs some tools to facilitate this process and make this possible.

- python ethereum-ipc-client (installed on your main python installation): https://github.com/pipermerriam/ethereum-ipc-client
- Nodejs web3 package (installed by the installers in ~/blockchain/nodejs): https://github.com/ethereum/web3.js/tree/master
- Nodejs gpio-stream package (installed by the installers in ~/blockchain/nodejs in Raspberry pi only): https://www.npmjs.com/package/gpio-stream
- Javascript web3.js is used to create the contract editor so the code can be used as example (Check the UI folder).

# Links
Understanding the Blockchain:
http://radar.oreilly.com/2015/01/understanding-the-blockchain.html


A 101 Noob Intro to Programming Smart Contracts on Ethereum:
https://medium.com/@ConsenSys/a-101-noob-intro-to-programming-smart-contracts-on-ethereum-695d15c1dab4#.hfiqgockk

Contract examples:
http://ether.fund/contracts/solidity

Solidity documentation:
https://github.com/ethereum/wiki/wiki/The-Solidity-Programming-Language
