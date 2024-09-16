import unittest
from unittest.mock import patch, MagicMock
from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic
import json

class TestMyWallet(unittest.TestCase):

    @patch('bitcoinlib.mnemonic.Mnemonic')
    @patch('bitcoinlib.wallets.Wallet')
    def test_wallet_creation(self, MockWallet, MockMnemonic):
        # Mock the Mnemonic instance and its generate method
        mock_mnemonic_instance = MockMnemonic.return_value
        mock_mnemonic_instance.generate.return_value = 'mocked mnemonic'

        # Mock the Wallet instance and its methods
        mock_wallet_instance = MockWallet.create.return_value
        mock_key_instance = MagicMock()
        mock_key_instance.address = 'mocked_address'
        mock_key_instance.wif = 'mocked_private_key'
        mock_wallet_instance.get_key.return_value = mock_key_instance

        # Import the script to test
        import tests.my_wallet as my_wallet

        # Assertions to verify the behavior
        MockMnemonic.assert_called_once()
        mock_mnemonic_instance.generate.assert_called_once()
        MockWallet.create.assert_called_once_with('my_wallet', witness_type='segwit', keys='mocked mnemonic', network='testnet')
        mock_wallet_instance.get_key.assert_called_once()

        # Verify the JSON file content
        with open('py-wallet.json', 'r') as file:
            data = json.load(file)
            self.assertEqual(data['address'], 'mocked_address')
            self.assertEqual(data['privateKey'], 'mocked_private_key')

if __name__ == '__main__':
    unittest.main()