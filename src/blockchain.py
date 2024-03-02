import hashlib
import json
import logging
import sys
import time

from ecdsa import VerifyingKey, NIST256p

import utils


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class BlockChain:
    
    MINING_DIFFICULTY = 3
    MINING_SENDER = 'THE BLOCKCHAIN'
    MINING_REWARD = 1.0
    
    def __init__(self, blockchain_address=None, port=None):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address
        self.port = port
    
    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_transaction(self, sender, recipient, amount, sender_public_key=None, signature=None):
        transaction = utils.sorted_dict({
            'sender_blockchain_address': sender,
            'recipient_blockchain_address': recipient,
            'amount': float(amount)
        })
        if sender == self.MINING_SENDER:
            self.transaction_pool.append(transaction)
            return True
        if self.verify_transaction_signature(sender_public_key, signature, transaction):
            # if self.calculate_total_amount(sender) < float(amount):
            #     return False
            self.transaction_pool.append(transaction)
            return True
        return False
    
    def verify_transaction_signature(self, sender_public_key, signature, transaction):
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        signature_bytes = bytes().fromhex(signature)
        verifying_key = VerifyingKey.from_string(bytes().fromhex(sender_public_key), curve=NIST256p)
        verified_key = verifying_key.verify(signature_bytes, message)
        return verified_key
    
    def proof_of_work(self):
        last_block = self.chain[-1]
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(last_block)
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def valid_proof(self, transactions, previous_hash, nonce, difficulty=MINING_DIFFICULTY):
        guess = utils.sorted_dict({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        guess_hash = self.hash(guess)
        return guess_hash[:difficulty] == '0' * difficulty

    def mining(self):
        self.add_transaction(
            sender=self.MINING_SENDER,
            recipient=self.blockchain_address,
            amount=self.MINING_REWARD
        )
        last_block = self.chain[-1]
        previous_hash = self.hash(last_block)
        nonce = self.proof_of_work()
        self.create_block(nonce, previous_hash)
        logging.info('MINING SUCCESSFUL')
        return True
    
    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block['transactions']:
                amount = transaction['amount']
                if blockchain_address == transaction['recipient_blockchain_address']:
                    total_amount += amount
                if blockchain_address == transaction['sender_blockchain_address']:
                    total_amount -= amount
        return total_amount
