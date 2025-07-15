from __future__ import annotations
import typing
import toolcli
import flood

def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': ls_command,
        'help': 'list available tests',
        'args': [],  # Remove chain argument
    }

def ls_command() -> None:
    import toolstr

    styles = flood.user_io.styles

    # Get all available test generators (both Ethereum and Move)
    generators = flood.generators.get_test_generators()
    
    toolstr.print_text_box('Available Tests', style=styles.get('title'))
    
    # Group by type
    eth_tests = [name for name in generators if name.startswith('eth_')]
    move_tests = [name for name in generators if name.startswith('move_')]
    
    if eth_tests:
        print('\nEthereum Tests:')
        for test in sorted(eth_tests):
            print(f'  {test}')
    
    if move_tests:
        print('\nMove-based Chain Tests:')
        for test in sorted(move_tests):
            print(f'  {test}')
    