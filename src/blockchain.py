import hashlib
import json
import logging
import sys
import time

import utils


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class BlockChain:
    
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


def pprint(obj):
    print(json.dumps(obj, indent=2))


if __name__ == '__main__':
    bc = BlockChain()
    
    bc.add_transaction('A', 'B', 1.0)
    bc.add_transaction('B', 'C', 2.0)
    previous_hash = bc.hash(bc.chain[-1])
    bc.create_block(0, previous_hash)
    pprint(bc.chain)
    
