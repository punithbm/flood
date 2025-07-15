from __future__ import annotations
import typing
import json
import flood

def generate_calls_move_get_account(
    n_calls: int,
    random_seed: flood.RandomSeed | None = None,
    **kwargs
) -> typing.Sequence[flood.Call]:
    """Generate calls for Move-based chain /v1/accounts/{address}"""
    rng = flood.generators.get_rng(random_seed=random_seed)
    addresses = _generate_valid_move_addresses(n_calls, rng)
    
    return [
        {
            'method': 'GET',
            'url': f'/v1/accounts/{address}',
            'header': {'Content-Type': ['application/json']},
            'body': ''
        }
        for address in addresses
    ]

def generate_calls_move_get_account_resources(
    n_calls: int,
    random_seed: flood.RandomSeed | None = None,
    **kwargs
) -> typing.Sequence[flood.Call]:
    """Generate calls for Move-based chain /v1/accounts/{address}/resources"""
    rng = flood.generators.get_rng(random_seed=random_seed)
    addresses = _generate_valid_move_addresses(n_calls, rng)
    
    return [
        {
            'method': 'GET',
            'url': f'/v1/accounts/{address}/resources',
            'header': {'Content-Type': ['application/json']},
            'body': ''
        }
        for address in addresses
    ]

def generate_calls_move_get_transactions(
    n_calls: int,
    random_seed: flood.RandomSeed | None = None,
    **kwargs
) -> typing.Sequence[flood.Call]:
    """Generate calls for Move-based chain /v1/transactions"""
    rng = flood.generators.get_rng(random_seed=random_seed)
    limits = rng.integers(1, 100, size=n_calls)
    
    return [
        {
            'method': 'GET',
            'url': f'/v1/transactions?limit={limit}',
            'header': {'Content-Type': ['application/json']},
            'body': ''
        }
        for limit in limits
    ]

def generate_calls_move_get_ledger_info(
    n_calls: int,
    random_seed: flood.RandomSeed | None = None,
    **kwargs
) -> typing.Sequence[flood.Call]:
    """Generate calls for Move-based chain /v1/"""
    return [
        {
            'method': 'GET',
            'url': '/v1/',
            'header': {'Content-Type': ['application/json']},
            'body': ''
        }
        for _ in range(n_calls)
    ]

def generate_calls_move_get_block_by_height(
    n_calls: int,
    random_seed: flood.RandomSeed | None = None,
    **kwargs
) -> typing.Sequence[flood.Call]:
    """Generate calls for Move-based chain /v1/blocks/by_height/{height}"""
    rng = flood.generators.get_rng(random_seed=random_seed)
    heights = rng.integers(1, 5000000, size=n_calls)
    
    return [
        {
            'method': 'GET',
            'url': f'/v1/blocks/by_height/{height}',
            'header': {'Content-Type': ['application/json']},
            'body': ''
        }
        for height in heights
    ]

def generate_calls_move_simulate_transaction(
    n_calls: int,
    random_seed: flood.RandomSeed | None = None,
    **kwargs
) -> typing.Sequence[flood.Call]:
    """Generate calls for Move-based chain POST /v1/transactions/simulate"""
    rng = flood.generators.get_rng(random_seed=random_seed)
    senders = _generate_valid_move_addresses(n_calls, rng)
    recipients = _generate_valid_move_addresses(n_calls, rng)
    amounts = rng.integers(1, 10000, size=n_calls)
    
    calls = []
    for i in range(n_calls):
        transaction_payload = {
            "sender": senders[i],
            "sequence_number": str(rng.integers(0, 1000)),
            "max_gas_amount": str(rng.integers(1000, 10000)),
            "gas_unit_price": str(rng.integers(1, 100)),
            "expiration_timestamp_secs": str(1700000000 + rng.integers(0, 86400)),
            "payload": {
                "type": "entry_function_payload",
                "function": "0x1::coin::transfer",
                "type_arguments": ["0x1::aptos_coin::AptosCoin"],
                "arguments": [recipients[i], str(amounts[i])]
            }
        }
        
        calls.append({
            'method': 'POST',
            'url': '/v1/transactions/simulate',
            'header': {'Content-Type': ['application/json']},
            'body': json.dumps(transaction_payload)
        })
    
    return calls

def _generate_valid_move_addresses(n_addresses: int, rng) -> typing.List[str]:
    """Generate valid Move blockchain addresses (32-byte hex strings)"""
    # Common Move blockchain addresses (works for Aptos, Sui, etc.)
    real_addresses = [
        "0x1",  # Framework account
        "0x2",  # Token account
        "0x3",  # Coin account
        "0x4",  # Names account
        "0xa",  # Common test address
        "0xf",  # Another common address
        # Real mainnet addresses (these are Aptos examples, but format is similar for Move chains)
        "0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12",
        "0x61d2c22a6cb7831bee0f48363b0eec92369357aece0244bd9b8740157922da8",
        "0x2c7bccf7b31baf770fdbcc768d9e9cb3d87805e255355df5db32ac9a669010a2",
        "0x5a97986a9d031c4567e15b797be516910cfcb4156312482efc6a19c0a30c948",
        "0x7968dab936c1bad187c60ce4082f307d030d780e91e694ae03aef16aba73f30",
    ]
    
    # For addresses that need to be full 32-byte format
    full_addresses = []
    for addr in real_addresses:
        if len(addr) < 66:  # 0x + 64 hex chars = 66 total
            # Pad with zeros to make it 32 bytes (64 hex chars)
            if addr.startswith('0x'):
                addr = addr[2:]  # Remove 0x
            addr = addr.zfill(64)  # Pad with leading zeros
            addr = '0x' + addr
        full_addresses.append(addr)
    
    # Generate additional random addresses if needed
    while len(full_addresses) < n_addresses:
        # Generate random 32-byte address
        random_bytes = rng.bytes(32)
        random_addr = '0x' + random_bytes.hex()
        full_addresses.append(random_addr)
    
    return rng.choice(full_addresses, size=n_addresses, replace=True).tolist() 