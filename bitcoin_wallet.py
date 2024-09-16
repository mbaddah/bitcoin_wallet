import os
from bitcoinlib.wallets import Wallet, wallets_list, wallet_delete
from bitcoinlib.mnemonic import Mnemonic

def create_wallet(wallet_name):

    # Create an instance of Mnemonic
    mnemonic_instance = Mnemonic()

    # Generate a new mnemonic
    mnemonic = mnemonic_instance.generate()

    # Create a new wallet from the mnemonic
    wallet = Wallet.create(wallet_name, witness_type='segwit', keys=mnemonic, network='testnet')

    # Get the first key in the wallet
    key = wallet.get_key()

    # Print and save wallet details
    print("| Public Address |", key.address, "|" )
    print("| Private Key |", key.wif , "|" )

    temp_dir = 'wallets'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    file_path = os.path.join(temp_dir, wallet_name + '.json')

    with open(file_path, 'w') as file:
        file.write(f'{{"address": "{key.address}", "privateKey": "{key.wif}"}}')

    load_wallet(wallet_name)

def load_wallet(wallet_name):
    #Load an existing wallet by name
    wallet = Wallet(wallet_name)

    # Get the first key in the wallet
    key = wallet.get_key()

    # Print wallet details
    print("Wallet Name:", wallet.name)
    print("Public Address:", key.address)
    print("Private Key:", key.wif)

    # Scan the wallet
    wallet.scan()
    # Shows wallet information, keys, transactions and UTXO's
    wallet.info()

def list_wallets():
    # List all existing wallets
    print("List of existing Wallets:")
    for wallet_name in wallets_list():
        print(wallet_name)

def delete_wallet(wallet_name):
    wallet_delete(wallet_name)
    print(f"Wallet '{wallet_name}' deleted")


def delete_all_wallets():
    # List all existing wallets
    for wallet_name in wallets_list():
        print(f"Deleting wallet: {wallet_name}")
        wallet_delete(wallet_name['id'])
    print("All wallets deleted")

wallet_name = input("Enter wallet name:")
create_wallet(wallet_name)
load_wallet(wallet_name)
list_wallets()
delete_wallet(wallet_name)
# delete_all_wallets()
list_wallets()