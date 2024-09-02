# Blockchain Project with Wallet System and Smart Contracts

This project implements a simple blockchain system with integrated wallet and smart contract features, demonstrating basic concepts of blockchain technology, cryptocurrency transactions, and decentralized applications. It includes both a command-line interface and a web interface for interacting with the blockchain.

## Features

1. **Blockchain Implementation**: A basic blockchain structure with blocks, mining, and chain validation.
2. **Wallet System**: Create and manage wallets, check balances, and perform transactions.
3. **Smart Contracts**: Create and execute simple smart contracts with conditions and expirations.
4. **Web Interface**: Flask-based web application for easy interaction through a browser.
5. **Responsive UI**: Modern, user-friendly interface with Bootstrap styling.
6. **Transaction History**: View transaction history for individual wallets.
7. **API Endpoints**: RESTful API for programmatic interaction with the blockchain.

## Project Structure

```
blockchain_project/
│
├── blockchain.py         # Core blockchain implementation
├── app.py                # Flask web application
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
│
└── templates/
    └── index.html        # Web interface HTML template
```

## Components

### Blockchain (blockchain.py)

- `Block` class: Represents individual blocks in the chain.
- `Wallet` class: Manages individual wallets with unique addresses and balances.
- `SmartContract` class: Implements simple smart contracts with conditions.
- `Blockchain` class: Handles overall blockchain operations.

### Web Application (app.py)

Flask application providing API endpoints and serving the web interface.

### Web Interface (templates/index.html)

HTML file for the frontend of the web application, featuring a responsive design with Bootstrap.

## Setup and Installation

1. Ensure you have Python 3.12 installed on your system. You can use pyenv to manage Python versions:
   ```
   pyenv install 3.12.0
   pyenv global 3.12.0
   ```

2. Clone the repository:
   ```
   git clone https://github.com/yourusername/blockchain_project.git
   cd blockchain_project
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   Dependencies:
   - Flask (2.3.2): Web framework for building the application
   - flask-cors (3.0.10): Extension for handling Cross Origin Resource Sharing (CORS)
   - uuid (1.30): For generating unique identifiers

5. Run the Flask application:
   ```
   python app.py
   ```

6. Access the web interface:
   Open a web browser and navigate to `http://localhost:5000`

## Configuration

The application doesn't require any specific configuration or environment variables. However, you can modify the following in `app.py` if needed:

- `host`: Change from '0.0.0.0' to 'localhost' for local-only access
- `port`: Change from 5000 to any other available port

## Usage Instructions (Web Interface)

1. **Create a new wallet**: Click the "Create Wallet" button in the Wallet Operations section.
2. **Check wallet balance**: Enter a wallet address and click "Check Balance" in the Wallet Operations section.
3. **Make a transaction**: Fill in the sender's address, recipient's address, and amount in the Make Transaction section, then click "Send Transaction".
4. **Mine a new block**: Enter a miner's wallet address in the Mine New Block section and click "Mine Block".
5. **View the blockchain**: Click "View Blockchain" in the Blockchain Operations section to see all blocks in the chain.
6. **Validate the blockchain**: Click "Validate Blockchain" in the Blockchain Operations section to check if the blockchain is valid.
7. **View transaction history**: Enter a wallet address in the Transaction History section and click "View History" to see all transactions for that wallet.
8. **Create a smart contract**: Fill in the contract details in the Smart Contracts section and click "Create Contract".
9. **Execute a smart contract**: Enter the contract ID in the Smart Contracts section and click "Execute Contract".
10. **View all smart contracts**: Click "View All Contracts" in the Smart Contracts section.

## API Endpoints

- POST `/wallet/new`: Create a new wallet
- GET `/wallet/balance/<address>`: Get balance for a wallet
- POST `/transaction/new`: Add a new transaction
- POST `/mine`: Mine a new block
- GET `/chain`: View the entire blockchain
- GET `/chain/valid`: Check if the blockchain is valid
- GET `/wallet/history/<address>`: Get transaction history for a wallet
- POST `/smart-contract/new`: Create a new smart contract
- POST `/smart-contract/execute/<contract_id>`: Execute a smart contract
- GET `/smart-contracts`: Get all smart contracts

## UI/UX Features

- Responsive design using Bootstrap for optimal viewing on various devices
- Intuitive navigation with a sidebar menu
- Card-based layout for clear separation of different functionalities
- Interactive tooltips for better user guidance
- Real-time feedback on user actions with loading indicators

## Troubleshooting

- If you encounter a "Address already in use" error, change the port number in `app.py`.
- Ensure all dependencies are correctly installed by running `pip freeze` and comparing with `requirements.txt`.
- If you face CORS issues, make sure the Flask-CORS extension is properly installed and configured.

## Known Issues and Limitations

1. **Smart Contract Execution**: The current implementation of smart contracts has issues with balance updates. When executing a smart contract, the recipient's wallet balance is not being updated correctly.
2. **Security**: This is a simplified implementation and lacks many security features required for a production-ready blockchain system. It should not be used for real-world transactions.
3. **Scalability**: The current implementation stores all blockchain data in memory, which is not suitable for large-scale use.
4. **Consensus Mechanism**: The project uses a simple Proof of Work mechanism and lacks more advanced consensus algorithms used in production blockchains.
5. **Smart Contract Functionality**: The smart contracts implemented here are basic and do not provide the full functionality or security features of production-grade smart contract platforms.

## Future Improvements

1. Implement proper balance updates for smart contract executions.
2. Add more robust error handling and input validation.
3. Implement a persistent storage solution for blockchain data.
4. Enhance the smart contract functionality to support more complex operations.
5. Implement additional security measures, such as transaction signing and verification.

## Note

This project is intended for educational purposes to demonstrate basic blockchain concepts. It should not be used as a basis for a production blockchain system without significant enhancements in security, scalability, and functionality.
