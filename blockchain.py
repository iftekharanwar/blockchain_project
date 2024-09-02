import hashlib
import time
import uuid
import datetime
import json
import os

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Wallet:
    def __init__(self):
        self.address = str(uuid.uuid4())
        self.balance = 0

class SmartContract:
    def __init__(self, contract_id, sender, recipient, amount, conditions, actions, expiration):
        self.id = contract_id
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.conditions = [int(condition) for condition in conditions]
        self.actions = actions
        self.expiration = int(expiration)
        self.executed = False

    def check_conditions(self):
        current_time = int(datetime.datetime.now().timestamp())
        return all(condition <= current_time for condition in self.conditions) and current_time <= self.expiration

    def execute_actions(self, blockchain):
        for action in self.actions:
            action(blockchain, self)

    def __str__(self):
        conditions_str = ", ".join(map(str, self.conditions))
        return f"Contract {self.id}: {self.sender} -> {self.recipient}, Amount: {self.amount}, Conditions: [{conditions_str}], Actions: {len(self.actions)}, Expiration: {self.expiration}, Executed: {self.executed}"

class Blockchain:
    def __init__(self, contract_file='smart_contracts.json', wallet_file='wallets.json'):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.wallets = {}
        self.mining_reward = 1
        self.smart_contracts = {}
        self.contract_file = contract_file
        self.wallet_file = wallet_file
        self.load_smart_contracts()
        self.load_wallets()

    def create_genesis_block(self):
        return Block(0, [], int(time.time()), "0")

    def create_wallet(self):
        wallet = Wallet()
        self.wallets[wallet.address] = wallet
        self.save_wallets()  # Save wallets after creating a new one
        return wallet.address

    def get_wallet(self, address):
        return self.wallets.get(address)

    def get_balance(self, address):
        return self.wallets[address].balance

    def add_to_wallet(self, address, amount):
        self.wallets[address].balance += amount

    def get_latest_block(self):
        return self.chain[-1]

    def transfer(self, sender_address, recipient_address, amount):
        import logging
        sender_wallet = self.get_wallet(sender_address)
        recipient_wallet = self.get_wallet(recipient_address)

        if sender_wallet is None or recipient_wallet is None:
            logging.error(f"Transfer failed: Invalid wallet address")
            return False

        if sender_wallet.balance < amount:
            logging.warning(f"Transfer failed: Insufficient balance. Required: {amount}, Available: {sender_wallet.balance}")
            return False

        sender_wallet.balance -= amount
        recipient_wallet.balance += amount
        logging.info(f"Transfer successful: {sender_address} -> {recipient_address}, Amount: {amount}")
        return True

    def add_transaction(self, sender_address, recipient_address, amount):
        import logging
        logging.info(f"Attempting to add transaction: {sender_address} -> {recipient_address}, Amount: {amount}")

        if self.transfer(sender_address, recipient_address, amount):
            self.pending_transactions.append({
                'sender': sender_address,
                'recipient': recipient_address,
                'amount': amount,
                'timestamp': int(time.time())
            })
            logging.info("Transaction added to pending transactions")
            return True
        else:
            logging.warning("Transaction failed")
            return False

    def mine_pending_transactions(self, miner_address):
        # Check if miner's wallet exists, create if it doesn't
        if miner_address not in self.wallets:
            wallet = Wallet()
            wallet.address = miner_address
            self.wallets[miner_address] = wallet
            print(f"Created new wallet for miner: {miner_address}")

        # Apply mining reward first
        mining_reward = self.mining_reward
        self.add_to_wallet(miner_address, mining_reward)
        print(f"Mining reward of {mining_reward} applied to miner's wallet: {miner_address}")

        # Process transactions after applying the reward
        valid_transactions = []
        for transaction in self.pending_transactions:
            if transaction['sender'] != "0":  # Not a mining reward
                if self.transfer(transaction['sender'], transaction['recipient'], transaction['amount']):
                    valid_transactions.append(transaction)
                    print(f"Transaction from {transaction['sender']} to {transaction['recipient']} of {transaction['amount']} processed successfully.")
                else:
                    print(f"Transaction from {transaction['sender']} to {transaction['recipient']} of {transaction['amount']} failed.")
            else:
                valid_transactions.append(transaction)

        # Create and mine the new block with valid transactions
        block = Block(len(self.chain), valid_transactions, int(time.time()), self.get_latest_block().hash)
        block.mine_block(self.difficulty)

        print("Block mined!")
        self.chain.append(block)

        # Clear pending transactions
        self.pending_transactions = []

        # Save wallet data after mining and processing transactions
        self.save_wallets()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_wallet_transactions(self, address):
        transactions = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction['sender'] == address or transaction['recipient'] == address:
                    transactions.append(transaction)
        return transactions

    def create_smart_contract(self, sender, recipient, amount, conditions, actions, expiration):
        contract_id = str(uuid.uuid4())
        contract = SmartContract(contract_id, sender, recipient, amount, conditions, actions, expiration)
        self.smart_contracts[contract_id] = contract
        self.save_smart_contracts()  # Save contracts after creating a new one
        return contract_id

    def execute_smart_contract(self, contract_id):
        import logging
        logging.info(f"Attempting to execute smart contract with ID: {contract_id}")
        contract = self.smart_contracts.get(contract_id)
        if contract:
            logging.info(f"Contract found: {contract}")
            current_time = int(datetime.datetime.now().timestamp())
            logging.info(f"Current time: {current_time}")

            logging.info(f"Validating sender's wallet address: {contract.sender}")
            sender_wallet = self.get_wallet(contract.sender)
            if sender_wallet is None:
                logging.error(f"Sender's wallet not found: {contract.sender}")
                return False

            logging.info(f"Evaluating contract conditions: {contract.conditions}")
            if all(condition <= current_time for condition in contract.conditions):
                logging.info("All contract conditions met. Attempting to execute actions.")
                sender_balance = self.get_balance(contract.sender)
                logging.info(f"Sender's current balance: {sender_balance}")

                if sender_balance >= contract.amount:
                    if self.transfer(contract.sender, contract.recipient, contract.amount):
                        for index, action in enumerate(contract.actions):
                            logging.info(f"Executing action {index + 1}/{len(contract.actions)}: {action}")
                            try:
                                if not action(self, contract):
                                    logging.error(f"Action execution failed: {action}")
                                    return False
                            except Exception as e:
                                logging.error(f"Exception during action execution: {str(e)}")
                                return False

                        contract.executed = True
                        del self.smart_contracts[contract_id]
                        self.save_smart_contracts()  # Save updated contracts to file
                        logging.info(f"Smart contract executed successfully. All actions completed.")
                        return True
                    else:
                        logging.error(f"Failed to transfer funds for smart contract execution")
                        return False
                else:
                    logging.warning(f"Insufficient balance. Required: {contract.amount}, Available: {sender_balance}")
                    return False
            else:
                logging.warning(f"Contract conditions not met. Current time: {current_time}")
        else:
            logging.warning(f"Contract with ID {contract_id} not found in smart_contracts: {list(self.smart_contracts.keys())}")
        return False

    def get_smart_contracts(self):
        return list(self.smart_contracts.values())

    def save_smart_contracts(self):
        with open(self.contract_file, 'w') as f:
            json.dump({k: v.__dict__ for k, v in self.smart_contracts.items()}, f)

    def load_smart_contracts(self):
        if os.path.exists(self.contract_file):
            with open(self.contract_file, 'r') as f:
                contracts_data = json.load(f)
                self.smart_contracts = {}
                for k, v in contracts_data.items():
                    # Handle backwards compatibility for single 'condition'
                    conditions = v.get('conditions', [v.get('condition')] if 'condition' in v else [])
                    conditions = [int(c) for c in conditions if c is not None]
                    actions = v.get('actions', [])
                    contract = SmartContract(
                        contract_id=k,
                        sender=v.get('sender'),
                        recipient=v.get('recipient'),
                        amount=float(v.get('amount', 0)),
                        conditions=conditions,
                        actions=actions,
                        expiration=int(v.get('expiration', 0))
                    )
                    contract.executed = v.get('executed', False)
                    self.smart_contracts[k] = contract
        else:
            self.smart_contracts = {}

    def save_wallets(self):
        with open('wallets.json', 'w') as f:
            json.dump({k: v.__dict__ for k, v in self.wallets.items()}, f)

    def load_wallets(self):
        if os.path.exists('wallets.json'):
            with open('wallets.json', 'r') as f:
                wallets_data = json.load(f)
                self.wallets = {k: Wallet() for k in wallets_data.keys()}
                for k, v in wallets_data.items():
                    self.wallets[k].__dict__.update(v)
        else:
            self.wallets = {}

def main():
    my_blockchain = Blockchain()

    # Create wallets
    alice_wallet = my_blockchain.create_wallet()
    bob_wallet = my_blockchain.create_wallet()
    charlie_wallet = my_blockchain.create_wallet()
    miner_wallet = my_blockchain.create_wallet()

    # Add initial balance to Alice's wallet
    my_blockchain.add_to_wallet(alice_wallet, 100)

    print(f"Alice's initial balance: {my_blockchain.get_balance(alice_wallet)}")
    print(f"Bob's initial balance: {my_blockchain.get_balance(bob_wallet)}")

    my_blockchain.add_transaction(alice_wallet, bob_wallet, 50)
    my_blockchain.add_transaction(bob_wallet, charlie_wallet, 25)

    print("Mining block 1...")
    my_blockchain.mine_pending_transactions(miner_wallet)

    print(f"Alice's balance after transactions: {my_blockchain.get_balance(alice_wallet)}")
    print(f"Bob's balance after transactions: {my_blockchain.get_balance(bob_wallet)}")
    print(f"Charlie's balance after transactions: {my_blockchain.get_balance(charlie_wallet)}")
    print(f"Miner's balance after mining: {my_blockchain.get_balance(miner_wallet)}")

    my_blockchain.add_transaction(charlie_wallet, alice_wallet, 10)

    print("Mining block 2...")
    my_blockchain.mine_pending_transactions(miner_wallet)

    print(f"Alice's final balance: {my_blockchain.get_balance(alice_wallet)}")
    print(f"Bob's final balance: {my_blockchain.get_balance(bob_wallet)}")
    print(f"Charlie's final balance: {my_blockchain.get_balance(charlie_wallet)}")
    print(f"Miner's final balance: {my_blockchain.get_balance(miner_wallet)}")

    print(f"Blockchain valid? {my_blockchain.is_chain_valid()}")

    # Print the blockchain
    for block in my_blockchain.chain:
        print(f"Block #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Transactions: {block.transactions}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("\n")

if __name__ == "__main__":
    main()
