from __future__ import annotations
import typing
import flood

# This should import from the object generators
from flood.generators.object_generators.move_generators import (
    generate_calls_move_get_account,
    generate_calls_move_get_transactions,
    generate_calls_move_get_account_resources,
    generate_calls_move_get_ledger_info,
    generate_calls_move_get_block_by_height,
    generate_calls_move_simulate_transaction,
)

# And define the test generators that flood looks for
def generate_test_move_get_account(
    *,
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    network: str,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
    random_seed: flood.RandomSeed | None = None,
) -> typing.Sequence[flood.VegetaAttack]:
    n_calls = flood.tests.load_tests.estimate_call_count(
        rates=rates, duration=duration, durations=durations
    )
    calls = generate_calls_move_get_account(
        n_calls=n_calls,
        random_seed=random_seed,
    )
    return flood.tests.load_tests.create_load_test(
        calls=calls,
        rates=rates,
        duration=duration,
        durations=durations,
        vegeta_args=vegeta_args,
    )

def generate_test_move_get_account_resources(
    *,
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    network: str,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
    random_seed: flood.RandomSeed | None = None,
) -> typing.Sequence[flood.VegetaAttack]:
    n_calls = flood.tests.load_tests.estimate_call_count(
        rates=rates, duration=duration, durations=durations
    )
    calls = generate_calls_move_get_account_resources(
        n_calls=n_calls,
        random_seed=random_seed,
    )
    return flood.tests.load_tests.create_load_test(
        calls=calls,
        rates=rates,
        duration=duration,
        durations=durations,
        vegeta_args=vegeta_args,
    )

def generate_test_move_get_transactions(
    *,
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    network: str,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
    random_seed: flood.RandomSeed | None = None,
) -> typing.Sequence[flood.VegetaAttack]:
    n_calls = flood.tests.load_tests.estimate_call_count(
        rates=rates, duration=duration, durations=durations
    )
    calls = generate_calls_move_get_transactions(
        n_calls=n_calls,
        random_seed=random_seed,
    )
    return flood.tests.load_tests.create_load_test(
        calls=calls,
        rates=rates,
        duration=duration,
        durations=durations,
        vegeta_args=vegeta_args,
    )

def generate_test_move_get_ledger_info(
    *,
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    network: str,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
    random_seed: flood.RandomSeed | None = None,
) -> typing.Sequence[flood.VegetaAttack]:
    n_calls = flood.tests.load_tests.estimate_call_count(
        rates=rates, duration=duration, durations=durations
    )
    calls = generate_calls_move_get_ledger_info(
        n_calls=n_calls,
        random_seed=random_seed,
    )
    return flood.tests.load_tests.create_load_test(
        calls=calls,
        rates=rates,
        duration=duration,
        durations=durations,
        vegeta_args=vegeta_args,
    )

def generate_test_move_get_block_by_height(
    *,
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    network: str,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
    random_seed: flood.RandomSeed | None = None,
) -> typing.Sequence[flood.VegetaAttack]:
    n_calls = flood.tests.load_tests.estimate_call_count(
        rates=rates, duration=duration, durations=durations
    )
    calls = generate_calls_move_get_block_by_height(
        n_calls=n_calls,
        random_seed=random_seed,
    )
    return flood.tests.load_tests.create_load_test(
        calls=calls,
        rates=rates,
        duration=duration,
        durations=durations,
        vegeta_args=vegeta_args,
    )

def generate_test_move_simulate_transaction(
    *,
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    network: str,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
    random_seed: flood.RandomSeed | None = None,
) -> typing.Sequence[flood.VegetaAttack]:
    n_calls = flood.tests.load_tests.estimate_call_count(
        rates=rates, duration=duration, durations=durations
    )
    calls = generate_calls_move_simulate_transaction(
        n_calls=n_calls,
        random_seed=random_seed,
    )
    return flood.tests.load_tests.create_load_test(
        calls=calls,
        rates=rates,
        duration=duration,
        durations=durations,
        vegeta_args=vegeta_args,
    ) 