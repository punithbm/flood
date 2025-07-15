from __future__ import annotations

import typing
import time

import flood
from . import single_runner_io
from . import single_runner_summary

def run(
    test_name: str,
    mode: flood.LoadTestMode | None = None,
    nodes: typing.Sequence[str] | None = None,
    metrics: typing.Sequence[str] | None = None,
    random_seed: int | None = None,
    verbose: bool = True,
    rates: typing.Sequence[int] | None = None,
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
    output_dir: str | None = None,
    dry: bool = False,
    debug: bool = False,
) -> None:
    """Run a single load test"""
    
    t_start = time.time()
    
    if include_deep_output is None:
        include_deep_output = []
    if deep_check and 'metrics' not in include_deep_output:
        include_deep_output = list(include_deep_output) + ['metrics']
    
    # Convert duration to durations for consistency
    durations = [duration] if duration is not None else None
    
    # Get test parameters using original logic
    rates, durations, vegeta_args = _get_single_test_parameters(
        test=None,
        rates=rates,
        duration=duration,
        durations=durations,
        mode=mode,
        vegeta_args=vegeta_args,
    )
    
    # Create output directory if not provided
    if output_dir is None:
        import tempfile
        output_dir = tempfile.mkdtemp(prefix='flood_')
    
    # Print preamble
    if verbose:
        single_runner_summary._print_single_run_preamble_copy(
            test_name=test_name,
            rerun_of=None,
            rates=rates,
            durations=durations,
            vegeta_args=vegeta_args,
            output_dir=output_dir,
        )
    
    # Parse nodes
    nodes_parsed = flood.user_io.parse_nodes(
        nodes, verbose=verbose, request_metadata=True
    )
    
    # Generate test parameters
    test_parameters = {
        'flood_version': flood.get_flood_version(),
        'test_name': test_name,
        'rates': rates,
        'durations': durations,
        'vegeta_args': vegeta_args,
        'network': flood.user_io.parse_nodes_network(nodes_parsed),
        'random_seed': random_seed,
    }
    
    # Save test to disk
    flood.runners.single_runner.single_runner_io._save_single_run_test(
        test_name=test_name,
        output_dir=output_dir,
        test_parameters=test_parameters,
    )
    
    # Skip dry run
    if dry:
        print()
        print('[dry run, exitting]')
        return {
            'output_dir': output_dir,
            'test': None,
            'test_parameters': test_parameters,
            'payload': {
                'results': [],
                'nodes': {},
                'test_parameters': test_parameters,
            }
        }
    
    # Run tests
    if verbose:
        single_runner_summary._print_run_start()
    results = flood.run_load_tests(
        nodes=nodes_parsed,
        test=test_parameters,
        verbose=verbose,
        include_deep_output=include_deep_output,
    )
    
    # Output results to file
    payload = single_runner_io._save_single_run_results(
        output_dir=output_dir,
        nodes=nodes_parsed,
        results=results,
        figures=figures,
        test_name=test_name,
        t_run_start=t_start,
        t_run_end=time.time(),
    )
    
    # Print summary
    if verbose:
        try:
            single_runner_summary._print_single_run_conclusion(
                output_dir=output_dir,
                results=results,
                metrics=metrics,
                verbose=verbose,
                figures=figures,
                deep_check=deep_check,
            )
        except Exception as e:
            print(f"Summary display failed (results still saved): {e}")
            print(f"Results saved to: {output_dir}")
            print("Use 'flood report {output_dir}' to view results")
    
    return {
        'output_dir': output_dir,
        'test': None,
        'test_parameters': test_parameters,
        'payload': payload,
    }

def _get_single_test_parameters(
    test: flood.LoadTest | None = None,
    rates: typing.Sequence[int] | None = None,
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    mode: flood.LoadTestMode | None = None,
    vegeta_args: flood.VegetaArgsShorthand | None = None,
) -> tuple[
    typing.Sequence[int],
    typing.Sequence[int],
    flood.VegetaArgsShorthand | None,
]:
    if test is not None:
        test_data = flood.user_io.parse_test_data(test=test)
        rates = test_data['rates']
        durations = test_data['durations']
        vegeta_args = test_data['vegeta_args']
    else:
        # Fix: If we have a single duration, replicate it for each rate
        if duration is not None and durations is None:
            if rates is not None:
                durations = [duration] * len(rates)  # Replicate duration for each rate
            else:
                durations = [duration]
        
        rates, durations = flood.generators.generate_timings(
            rates=rates,
            duration=duration,
            durations=durations,
            mode=mode,
        )
    return rates, durations, vegeta_args

