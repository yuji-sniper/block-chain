import hashlib
import json
import logging
import sys
import time

import utils


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class BlockChain:
    
    MINING_DIFFICULTY = 3
    MINING_SENDER = 'THE BLOCKCHAIN'
    MINING_REWARD = 1.0
    
    def __init__(self, blockchain_address=None):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address
    
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
                if blockchain_address == transaction['recipient']:
                    total_amount += amount
                if blockchain_address == transaction['sender']:
                    total_amount -= amount
        return total_amount


if __name__ == '__main__':
    my_blockchain_address = 'my_blockchain_address'
    bc = BlockChain(blockchain_address=my_blockchain_address)
    
    bc.add_transaction('A', 'B', 5.0)
    bc.mining()
    utils.pprint(bc.chain)
    
    bc.add_transaction('C', 'D', 6.0)
    bc.add_transaction('X', 'Y', 7.0)
    bc.mining()
    utils.pprint(bc.chain)

    print(bc.calculate_total_amount(my_blockchain_address))
