import os
import json
import math
import random
import subprocess

V2_GENESIS = """{
    "nonce": "0x0000000000000042",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "difficulty": "0x4000",
    "alloc": {},
    "coinbase": "0x0000000000000000000000000000000000000000",
    "timestamp": "0x00",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "extraData": "V2 Custom Ethereum Genesis Block",
    "gasLimit": "0xffffffff"
}"""

class Node(object):
    def __init__(self, identity=None, port=None, rpc_port=None, obj=None):
        if obj is None:
            if identity is None:
                self.identity = "node_%s" % int(math.floor(random.random()*100000))
            else:
                self.identity = identity
            if port is None:
                self.port = 30300
            else:
                self.port = port
            if rpc_port is None:
                self.rpc_port = 8000
            else:
                self.rpc_port = rpc_port
            self.data_dir = self.identity + "_data"
        else:
            self.fromObj(obj)

    def toObj(self):
        return {
            "identity": self.identity,
            "port": self.port,
            "rpc_port": self.rpc_port,
            "data_dir": self.data_dir
        }

    def toJSON(self):
        obj = self.toObj()
        return json.dumps(obj)

    def fromObj(self, obj):
        self.identity = obj["identity"]
        self.port = obj["port"]
        self.rpc_port = obj["rpc_port"]
        self.data_dir = obj["data_dir"]

    def fromJSON(self, json_str):
        obj = json.loads(json_str)
        self.fromObj(obj)

class BlockchainConfig(object):
    def __init__(self, path):
        self.path = os.path.expanduser(path)
        self.filename = "BlockchainConfig.json"

        #Default values
        self.nodes = []
        self.autodag = "false"
        self.rpc_port_start = 8000
        self.port_start = 30300
        self.genesis = "CustomGenesis.json"
        self.nat = "any"
        self.network_id = 1000
        self.bootnodes = ["enode://eb6e308b5194349790dc17a95068a1b1c8712c772ca7c3b679baacc3dd8cd8328a6608a7a32545a611e67159c0179e1498d182782b95f71fc1f4c78458fa48c7@52.30.156.83:30300"]


        if os.path.isdir(self.path):
            #print("Blockchain directory exists. All fine.")
            pass
        else:
            print("Creating Blockchain directory at %s" % self.path)
            os.mkdir(self.path)

        if os.path.exists(self.path + "/" + self.filename):
            #print("Config file found, reading it.")
            self.load()
        else:
            print("Creating config file at %s" % self.path + "/" + self.filename)
            self.save()

        if os.path.exists(self.path + "/" + self.genesis):
            #print("Genesis file found. All fine.")
            pass
        else:
            print("Creating genesis file at %s" % self.path + "/" + self.genesis)
            f = open(self.path + "/" + self.genesis,"w")
            f.write(V2_GENESIS)
            f.close()

    def save(self):
        f = open(self.path + "/" + self.filename, 'w')
        f.write(self.toJSON())
        f.close()

    def load(self):
        f = open(self.path + "/" + self.filename, 'r')
        json_str = f.read()
        f.close()
        obj = json.loads(json_str)
        self.fromObj(obj)

    def createNode(self, identity, create_account=True):
        identity = identity.replace(";", "").replace(" ", "_")
        print("Creating new ethereum node.")
        n = Node(identity=identity, port=self.port_start+len(self.nodes), rpc_port=self.rpc_port_start+len(self.nodes))
        print("Creating data directory %s" % self.path + "/" + n.data_dir)
        os.mkdir(self.path + "/" + n.data_dir)
        self.nodes.append(n)
        print("Saving configurations.")
        self.save()
        if create_account:
            print("Creating new account.")
            result = subprocess.call("geth " + self.getConfigString(n) + " account new", shell=True)
            if result != 0:
                print("Error occured while creating account.")

        print("All done.")
        print("Use: v2bc -i %s start" % identity)

    def fromObj(self, obj):
        for n in obj["nodes"]:
            self.nodes.append(Node(obj=n))

        self.autodag = obj["autodag"]
        self.rpc_port_start = obj["rpc_port_start"]
        self.port_start = obj["port_start"]
        self.genesis = obj["genesis"]
        self.nat = obj["nat"]
        self.network_id = obj["network_id"]
        self.bootnodes = obj["bootnodes"]

    def toObj(self):
        nodes_obj = []

        for n in self.nodes:
            nodes_obj.append(n.toObj())

        return {
            "nodes": nodes_obj,
            "autodag": self.autodag,
            "rpc_port_start": self.rpc_port_start,
            "port_start": self.port_start,
            "network_id": self.network_id,
            "genesis": self.genesis,
            "nat": self.nat,
            "bootnodes": self.bootnodes
        }

    def toJSON(self):
        obj = self.toObj()
        return json.dumps(obj)

    def getNodeById(self, id):
        for n in self.nodes:
            if n.identity == id:
                return n
        return None

    def getConfigString(self, node):
        return '--autodag="%(autodag)s" --identity="%(identity)s" --bootnodes="%(bootnodes)s" --genesis="%(genesis)s" --rpc --rpcapi="db,eth,net,web3" --rpcport="%(rpc_port)s" --rpccorsdomain="localhost" --datadir="%(data_dir)s" --port="%(port)s" --ipcapi="admin,db,eth,debug,miner,net,shh,txpool,personal,web3" --networkid="%(network_id)s" --nat="%(nat)s"' % {
            "autodag": self.autodag,
            "identity": node.identity,
            "bootnodes":" ".join(self.bootnodes),
            "genesis": self.path + "/" + self.genesis,
            "rpc_port": node.rpc_port,
            "port": node.port,
            "data_dir": self.path + "/" + node.data_dir,
            "network_id": self.network_id,
            "nat": self.nat,
        }

    def getIPCSocket(self, node):
        return self.path + "/" + node.data_dir + "/geth.ipc"
