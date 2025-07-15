
# flood

**flood** is a load testing tool for benchmarking EVM and Move based blockchain nodes over RPC.

**flood** measures the throughput, latency, and error rate of RPC endpoints. It can compare the performance of different node clients, different hardware configurations, and different RPC providers.

**flood** can run locally or in the cloud. It can also run differential (equality) tests to make sure that different nodes return the same results.

## Installation

```bash
pip install paradigm-flood
```

## Usage

### Basic Usage

**flood** can benchmark both Ethereum (EVM) and Move based blockchain nodes:

#### Ethereum Examples
```bash
# Benchmark eth_getBlockByNumber on a single node
flood eth_getBlockByNumber localhost:8545 --rates 10 100 1000 --duration 30

# Compare two nodes
flood eth_call node1=localhost:8545 node2=localhost:8546 --rates 1024 2048 4096

# Test multiple methods
flood eth_getLogs localhost:8545 --rates 64 128 256 512 1024
```

#### Move based Chain Examples (Aptos, Sui, etc.)
```bash
# Benchmark account queries on Aptos mainnet
flood move_get_account https://fullnode.mainnet.aptoslabs.com --rates 10 100 1000 --duration 30

# Test transaction simulation
flood move_simulate_transaction https://fullnode.mainnet.aptoslabs.com --rates 50 100 --duration 60

# Compare different Move based endpoints
flood move_get_ledger_info node1=https://fullnode.mainnet.aptoslabs.com node2=https://api.mainnet.aptoslabs.com --rates 100 200

# Test block queries
flood move_get_block_by_height https://fullnode.mainnet.aptoslabs.com --rates 25 50 100
```

### Available Test Methods

#### Ethereum (EVM) Methods
- `eth_getBlockByNumber` - Get block by number
- `eth_getBlockByHash` - Get block by hash  
- `eth_call` - Execute a call
- `eth_getBalance` - Get account balance
- `eth_getTransactionCount` - Get transaction count
- `eth_getTransactionByHash` - Get transaction by hash
- `eth_getTransactionReceipt` - Get transaction receipt
- `eth_getLogs` - Get event logs
- `eth_getCode` - Get contract code
- `eth_getStorageAt` - Get storage value
- `eth_feeHistory` - Get fee history
- `trace_block` - Trace block execution
- `trace_transaction` - Trace transaction execution
- `debug_traceBlockByNumber` - Debug trace block

#### Move based Chain Methods
- `move_get_account` - Get account information
- `move_get_account_resources` - Get account resources
- `move_get_transactions` - Get transactions
- `move_get_ledger_info` - Get ledger information
- `move_get_block_by_height` - Get block by height
- `move_simulate_transaction` - Simulate transaction execution

### List Available Tests

```bash
# List all available test methods
flood ls
```

### Advanced Usage

#### Load Testing Parameters
```bash
# Multiple rates and longer duration
flood move_get_account https://fullnode.mainnet.aptoslabs.com --rates 10 50 100 200 --duration 60

# Custom output directory
flood eth_getBlockByNumber localhost:8545 --rates 100 --duration 30 --output /tmp/my_test

# Dry run to see what requests will be made
flood move_simulate_transaction https://fullnode.mainnet.aptoslabs.com --rates 10 --duration 5 --dry
```

#### Generate Reports
```bash
# Run a test and save results
flood move_get_account https://fullnode.mainnet.aptoslabs.com --rates 50 100 --duration 30 --output /tmp/move_test

# Generate HTML report from results
flood report /tmp/move_test
```

### Multi-Chain Architecture

**flood** supports multiple blockchain architectures:

- **Ethereum (EVM)**: Uses JSON-RPC over HTTP POST with methods like `eth_getBlockByNumber`
- **Move based chains**: Uses REST API over HTTP GET/POST with endpoints like `/v1/accounts/{address}`

The tool automatically handles the different request formats:
- Ethereum: JSON-RPC payloads in request body
- Move chains: REST API with parameters in URL path and query strings

### Performance Metrics

**flood** measures:
- **Throughput**: Requests per second successfully processed
- **Latency**: Response time percentiles (p50, p90, p95, p99)
- **Error Rate**: Percentage of failed requests
- **Success Rate**: Percentage of successful requests

### Comparison Testing

Compare different nodes or providers:

```bash
# Compare Ethereum nodes
flood eth_call node1=localhost:8545 node2=localhost:8546 --rates 100 200

# Compare Move based endpoints  
flood move_get_account node1=https://fullnode.mainnet.aptoslabs.com node2=https://api.mainnet.aptoslabs.com --rates 50 100
```

### Cloud Usage

**flood** can run tests in the cloud for more realistic load testing scenarios. See the documentation for cloud deployment options.

## Example Workflows

### Ethereum Node Benchmarking

```bash
# 1. Test basic block queries
flood eth_getBlockByNumber localhost:8545 --rates 10 50 100 --duration 30

# 2. Test contract calls
flood eth_call localhost:8545 --rates 25 50 100 --duration 60

# 3. Generate comprehensive report
flood report /tmp/eth_test_results
```

### Move Chain Performance Testing

```bash
# 1. Test account queries
flood move_get_account https://fullnode.mainnet.aptoslabs.com --rates 20 50 100 --duration 30

# 2. Test transaction simulation
flood move_simulate_transaction https://fullnode.mainnet.aptoslabs.com --rates 10 25 50 --duration 60

# 3. Test ledger info (lightweight endpoint)
flood move_get_ledger_info https://fullnode.mainnet.aptoslabs.com --rates 100 200 500 --duration 30

# 4. Generate report
flood report /tmp/move_test_results
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

Licensed under either of Apache License, Version 2.0 or MIT license at your option.

