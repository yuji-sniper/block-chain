import logging
import sys
import time
import json


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class BlockChain:
    
    def __init__(self):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, 'init hash')
    
    def create_block(self, nonce, previous_hash):
        block = {
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        self.transaction_pool = []
        return block


def pprint(obj):
    print(json.dumps(obj, indent=2))


if __name__ == '__main__':
    bc = BlockChain()
    bc.create_block(1, 'hash1')
    bc.create_block(2, 'hash2')
    pprint(bc.chain)
