import pytest
from bitcoinlib.wallets import Wallet, wallets_list, wallet_delete
from bitcoin_wallet import create_wallet, load_wallet, list_wallets, delete_wallet

@pytest.fixture
def wallet_name():
    return "test_wallet"

def test_create_wallet(wallet_name):
    create_wallet(wallet_name)
    wallets = wallets_list()
    assert any(wallet['name'] == wallet_name for wallet in wallets), "Wallet was not created"

def test_load_wallet(wallet_name):
    create_wallet(wallet_name)
    wallet = Wallet(wallet_name)
    key = wallet.get_key()
    assert key.address is not None, "Wallet key address is None"
    assert key.wif is not None, "Wallet private key (WIF) is None"

def test_list_wallets(wallet_name, capsys):
    create_wallet(wallet_name)
    list_wallets()
    captured = capsys.readouterr()
    assert wallet_name in captured.out, "Wallet name not found in list_wallets output"

def test_delete_wallet(wallet_name):
    create_wallet(wallet_name)
    delete_wallet(wallet_name)
    wallets = wallets_list()
    assert not any(wallet['name'] == wallet_name for wallet in wallets), "Wallet was not deleted"

@pytest.fixture(autouse=True)
def cleanup_wallets():
    yield
    for wallet in wallets_list():
        wallet_delete(wallet['id'])
