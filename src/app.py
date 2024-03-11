from flask import Flask, jsonify

import blockchain
import wallet

app = Flask(__name__)

app.config['port'] = 5000

cache = {}
def get_blockchain():
    cached_blockchain = cache.get('blockchain')
    if not cached_blockchain:
        miners_wallet = wallet.Wallet()
        cache['blockchain'] = blockchain.BlockChain(
            blockchain_address=miners_wallet.blockchain_address,
            port=app.config['port']
        )
        app.logger.warning({
            'private_key': miners_wallet.private_key,
            'public_key': miners_wallet.public_key,
            'blockchain_address': miners_wallet.blockchain_address
        })
    return cache['blockchain']

@app.route('/chain', methods=['GET'])
def get_chain():
    block_chain = get_blockchain()
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain)
    }
    return jsonify(response), 200
