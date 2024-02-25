import hashlib
import json
import logging
import sys
import time

import utils


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class BlockChain:
    
    MINING_DIFFICULTY = 3
    
    def __init__(self):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))
    
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
    
    def add_transaction(self, sender, recipient, amount):
        transaction = utils.sorted_dict({
            'sender': sender,
            'recipient': recipient,
            'amount': float(amount)
        })
        self.transaction_pool.append(transaction)
        return True
    
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


if __name__ == '__main__':
    bc = BlockChain()
    
    bc.add_transaction('A', 'B', 1.0)
    bc.add_transaction('B', 'C', 2.0)
    previous_hash = bc.hash(bc.chain[-1])
    nonce = bc.proof_of_work()
    bc.create_block(nonce, previous_hash)
    utils.pprint(bc.chain)
