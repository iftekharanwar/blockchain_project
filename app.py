from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from blockchain import Blockchain
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wallet/new', methods=['POST'])
def create_wallet():
    address = blockchain.create_wallet()
    response = {'wallet_address': address}
    return jsonify(response), 201

@app.route('/wallet/balance/<address>', methods=['GET'])
def get_balance(address):
    try:
        balance = blockchain.get_balance(address)
        response = {'address': address, 'balance': balance}
        return jsonify(response), 200
    except KeyError:
        return jsonify({'error': 'Wallet not found'}), 404

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing values'}), 400

    sender = values['sender']
    recipient = values['recipient']
    amount = float(values['amount'])

    try:
        if blockchain.add_transaction(sender, recipient, amount):
            response = {'message': 'Transaction added successfully'}
            return jsonify(response), 201
        else:
            return jsonify({'error': 'Insufficient balance'}), 400
    except KeyError:
        return jsonify({'error': 'Invalid wallet address'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

@app.route('/mine', methods=['POST'])
def mine():
    values = request.get_json()
    if 'miner_address' not in values:
        return jsonify({'error': 'Missing miner address'}), 400

    miner_address = values['miner_address']
    blockchain.mine_pending_transactions(miner_address)
    response = {'message': 'New block mined successfully'}
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        })
    response = {
        'chain': chain_data,
        'length': len(chain_data)
    }
    return jsonify(response), 200

@app.route('/chain/valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid()
    response = {'valid': is_valid}
    return jsonify(response), 200

@app.route('/wallet/history/<address>', methods=['GET'])
def get_wallet_history(address):
    try:
        transactions = blockchain.get_wallet_transactions(address)
        response = {'address': address, 'transactions': transactions}
        return jsonify(response), 200
    except KeyError:
        return jsonify({'error': 'Wallet not found'}), 404

@app.route('/smart-contract/new', methods=['POST'])
def create_smart_contract():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'conditions', 'actions', 'expiration']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing values'}), 400

    try:
        conditions = [int(condition) for condition in values['conditions']]
        actions = values['actions']  # Assuming actions are defined as strings or function names
        contract_id = blockchain.create_smart_contract(
            values['sender'],
            values['recipient'],
            float(values['amount']),
            conditions,
            actions,
            int(values['expiration'])
        )
        response = {'message': 'Smart contract created successfully', 'contract_id': contract_id}
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error creating smart contract: {str(e)}'}), 500

@app.route('/smart-contract/execute/<contract_id>', methods=['POST'])
def execute_smart_contract(contract_id):
    app.logger.info(f"Attempting to execute smart contract with ID: {contract_id}")
    try:
        if blockchain.execute_smart_contract(contract_id):
            app.logger.info(f"Smart contract {contract_id} executed successfully")
            response = {'message': 'Smart contract executed successfully'}
            return jsonify(response), 200
        else:
            app.logger.warning(f"Smart contract {contract_id} execution failed")
            return jsonify({'error': 'Smart contract execution failed. Condition not met or contract not found.'}), 400
    except Exception as e:
        app.logger.error(f"Error executing smart contract {contract_id}: {str(e)}")
        return jsonify({'error': f'Smart contract execution error: {str(e)}'}), 500

@app.route('/smart-contracts', methods=['GET'])
def get_smart_contracts():
    contracts = blockchain.get_smart_contracts()
    response = {'smart_contracts': [vars(contract) for contract in contracts]}
    return jsonify(response), 200

if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app)
    app.run(host='0.0.0.0', port=5000)
