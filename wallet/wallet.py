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

# decoded = json.dumps(output)
# print(json.dumps(decoded, indent=4, sort_keys=True))

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# derive_wallets function test
derive_wallets(mnemonic,'BTC',3)

coins = {'eth','btc','btc-test'}
numderive = 3

keys = {}
for coin in coins:
    keys[coin]= derive_wallets(mnemonic, coin, numderive=3)

# store private keys
eth_PrivateKey = keys["eth"][0]['privkey']
btc_PrivateKey = keys['btc-test'][0]['privkey']

print(json.dumps(eth_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(btc_PrivateKey, indent=4, sort_keys=True))

# function to create transaction for eth or btc-test coin
def create_tx(coin, account, recipient, amount):
    if coin == ETH:
        
        gasEstimate = w3.eth.estimateGas(
            {"from": eth_account.address, "to": recipient, "value": amount}
    )
        return {
            "from": eth_account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_account.address),
        }
    elif coin == BTC-TEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
    
# function to sending transactions
def send_tx(account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

# function to convert privatekey into child key for account 
def priv_key_to_account(coin,priv_key):
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTC_TEST:
        return PrivateKeyTestnet(priv_key)

btc_acc = priv_key_to_account(BTC_TEST,btc_PrivateKey)

# Create btc-test transaction
create_tx(BTC_TEST,btc_acc,"37NFX8KWAQbaodUG6pE1hNUH1dXgkpzbyZ", 0.1)

# Send btc-test transaction
send_txn(BTC_TEST,btc_acc,"1C7pQrvWE54FpiyErnJR7sVB52rSiQGEiH", 0.1)

# Check if connected to blockchain. 
w3.isConnected()

# Check the Balance of the account with local mining blockchain
w3.eth.getBalance("02b567670d35f41e76ed160634bd890fbe8ac6c9ded0cdfe17631faeb60518c728")

# Create ETH transaction
create_tx(ETH,eth_acc,"0x06c9A379C6f4b11CeAda09c992C6d70498437c13", 1000)

# Send ETH transaction
send_txn(ETH, eth_acc,"0x06c9A379C6f4b11CeAda09c992C6d70498437c13", 1000)

# Check balance
w3.eth.getBalance("0x06c9A379C6f4b11CeAda09c992C6d70498437c13")