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
    figures: bool = True,
    **kwargs
) -> None:
    
    # Handle rates and durations properly
    if rates is None:
        rates = [100]  # default rate
    
    if duration is not None and durations is None:
        # If single duration provided, repeat it for each rate
        durations = [duration] * len(rates)
    elif duration is None and durations is None:
        # If no duration provided, use default for each rate
        durations = [30] * len(rates)
    elif duration is None and durations is not None:
        # durations already provided, use as-is
        pass
    else:
        # Both duration and durations provided, prefer durations
        durations = [duration] * len(rates)
    
    # Ensure rates and durations have same length
    if len(rates) != len(durations):
        if len(durations) == 1:
            # Repeat single duration for all rates
            durations = durations * len(rates)
        elif len(rates) == 1:
            # Repeat single rate for all durations
            rates = rates * len(durations)
        else:
            raise ValueError(f"Different number of rates ({len(rates)}) vs durations ({len(durations)})")
    
    try:
        # Create the test
        test = flood.generate_test(
            test_name=test_name,
            rates=rates,
            durations=durations,
            vegeta_args=vegeta_args,
            random_seed=random_seed,
            network='',
            flood_version=flood.get_flood_version(),
        )
        
        # Handle dry run
        if dry:
            print(f"Method: {test_name}")
            print(f"Available methods for move-based chains: {', '.join(['move_get_account', 'move_get_account_resources', 'move_get_transactions', 'move_get_ledger_info', 'move_get_block_by_height', 'move_simulate_transaction'])}")
            print(f"\nWould generate {len(test.attacks)} attacks:")
            for i, attack in enumerate(test.attacks):
                print(f"  Attack {i+1}: rate={attack.rate}, duration={attack.duration}, calls={attack.rate * attack.duration}")
                if attack.calls:
                    sample_call = attack.calls[0]
                    print(f"    Sample call: {sample_call}")
                    # Log the actual endpoint being called
                    if 'url' in sample_call:
                        print(f"    📍 Endpoint: {sample_call['method']} {sample_call['url']}")
                    if 'body' in sample_call and sample_call['body']:
                        print(f"    📦 Body: {sample_call['body'][:100]}...")
            return
        
        # Get nodes
        if nodes is None:
            nodes = ['localhost:8545']
        
        # Parse nodes properly
        parsed_nodes = flood.user_io.parse_nodes(
            nodes, verbose=verbose, request_metadata=True
        )
        
        # Log the endpoints that will be called
        if verbose:
            print(f"\n📍 Endpoint Information:")
            print(f"   Test: {test_name}")
            
            # Handle both dict and object test structures
            if hasattr(test, 'attacks') and test.attacks:
                attacks = test.attacks
            elif isinstance(test, dict) and 'attacks' in test:
                attacks = test['attacks']
            else:
                attacks = []
            
            if attacks and len(attacks) > 0:
                # Get first attack's first call as sample
                first_attack = attacks[0]
                if hasattr(first_attack, 'calls') and first_attack.calls:
                    sample_call = first_attack.calls[0]
                elif isinstance(first_attack, dict) and 'calls' in first_attack:
                    sample_call = first_attack['calls'][0]
                else:
                    sample_call = None
                
                if sample_call:
                    print(f"   Method: {sample_call.get('method', 'Unknown')}")
                    print(f"   URL Pattern: {sample_call.get('url', 'Unknown')}")
                    if sample_call.get('body'):
                        print(f"   Request Type: POST (with body)")
                    else:
                        print(f"   Request Type: GET (no body)")
                    
                    # Count total calls
                    total_calls = 0
                    for attack in attacks:
                        if hasattr(attack, 'calls'):
                            total_calls += len(attack.calls)
                        elif isinstance(attack, dict) and 'calls' in attack:
                            total_calls += len(attack['calls'])
                    
                    print(f"   Total calls across all attacks: {total_calls}")
                else:
                    print(f"   No sample calls available")
            else:
                print(f"   No attacks found in test")
            print()
        
        # Run the load test
        results = flood.run_load_tests(
            tests={'test': test},
            nodes=parsed_nodes,
            verbose=verbose,
        )
        
        # Save results if output_dir is specified
        if output_dir:
            single_runner_io._save_single_run_results(
                output_dir=output_dir,
                nodes=parsed_nodes,
                results=results,
                figures=figures,
                test_name=test_name,
                t_run_start=time.time(),
                t_run_end=time.time(),
            )
        
        # Display results - use the correct function name
        try:
            # Print basic results summary
            print("\n" + "="*50)
            print("LOAD TEST RESULTS")
            print("="*50)
            
            for node_name, node_results in results.items():
                # Clean up node name display
                display_name = node_name.replace('__test', '')
                print(f"\nNode: {display_name}")
                print("-" * 50)
                
                if isinstance(node_results, dict):
                    # Extract key metrics
                    target_rates = node_results.get('target_rate', rates)
                    actual_rates = node_results.get('actual_rate', [])
                    throughput = node_results.get('throughput', [])
                    success_rates = node_results.get('success', [])
                    status_codes = node_results.get('status_codes', [])
                    errors = node_results.get('errors', [])
                    
                    print(f"{'Target RPS':<12} {'Actual RPS':<12} {'Success RPS':<12} {'Success %':<10} {'Duration':<10}")
                    print("-" * 60)
                    
                    for i in range(len(target_rates)):
                        target_rate = target_rates[i] if i < len(target_rates) else 0
                        actual_rate = actual_rates[i] if i < len(actual_rates) else 0
                        success_rps = throughput[i] if i < len(throughput) else 0
                        success_pct = success_rates[i] * 100 if i < len(success_rates) else 0
                        duration = durations[i] if i < len(durations) else 0
                        
                        print(f"{target_rate:<12} {actual_rate:<12.1f} {success_rps:<12.1f} {success_pct:<10.1f} {duration}s")
                    
                    # Show error details
                    print(f"\n📊 Error Analysis:")
                    if status_codes:
                        for i, codes in enumerate(status_codes):
                            print(f"  Attack {i+1}: {codes}")
                    
                    if errors:
                        print(f"\n❌ Error Types:")
                        for i, error_list in enumerate(errors):
                            print(f"  Attack {i+1}: {error_list}")
                    
                    # Show latency info if available
                    if 'mean' in node_results:
                        mean_latency = node_results['mean']
                        p90_latency = node_results['p90']
                        p95_latency = node_results['p95']
                        
                        print(f"\n⏱️  Latency (seconds):")
                        print(f"{'Attack':<8} {'Mean':<8} {'P90':<8} {'P95':<8}")
                        print("-" * 32)
                        for i in range(len(mean_latency)):
                            print(f"{i+1:<8} {mean_latency[i]:<8.3f} {p90_latency[i]:<8.3f} {p95_latency[i]:<8.3f}")
                else:
                    print(f"Raw result: {node_results}")
                print()
            
            print("="*50)
            if all(throughput[i] == 0 for i in range(len(throughput))):
                print("❌ Load test completed with errors!")
                print("\n🔍 Troubleshooting:")
                print("   - Check if the server supports the endpoint")
                print("   - Verify the server is running and accessible")
                print("   - Check if authentication is required")
                print("   - Try a different endpoint (e.g., move_get_ledger_info)")
            else:
                print("✅ Load test completed successfully!")
            
            print("\n📊 Metrics Explained:")
            print("   - Target RPS: Requested load rate")
            print("   - Actual RPS: Actual request rate sent")
            print("   - Success RPS: Successful requests per second")
            print("   - Success %: Percentage of successful requests")
            
            if output_dir:
                print(f"\n📁 Results saved to: {output_dir}")
                print(f"📊 Generate report: flood report {output_dir}")
        
        except Exception as e:
            print(f"Summary display failed (results still saved): {e}")
            print(f"Debug info - Results: {results}")
            if output_dir:
                print(f"Results saved to: {output_dir}")
                print(f"Use 'flood report {output_dir}' to view results")
        
    except Exception as e:
        if debug:
            import pdb; pdb.set_trace()
        else:
            print(f"Error: {e}")

