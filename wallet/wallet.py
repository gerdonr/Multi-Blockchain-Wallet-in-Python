# import libraries
import subprocess
import json
from constants import *
from dotenv import load_dotenv
from bipwallet import wallet
from web3 import Web3
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

load_dotenv()

file_path = ".env"


command = './derive -g --mnemonic="smile tip enhance trade cotton foam wolf odor lava museum action wash" --cols=path,address,privkey,pubkey --format=json'

mnemonic = os.getenv('MNEMONIC', 'smile tip enhance trade cotton foam wolf odor lava museum action wash')

#create derive_wallets function
def derive_wallets(mnemonic,coin,numderive):
    command = 'php derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --format=json --coin={coin} --numderive={numderive}'
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
   
    keys = json.loads(output)
    return  keys

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# derive_wallets function test
derive_wallets(mnemonic,'BTC',3)

coins = {'eth','btc','btc-test'}
numderive = 3

keys = {}
for coin in coins:
    keys[coin]= derive_wallets(mnemonic, coin, numderive=3)