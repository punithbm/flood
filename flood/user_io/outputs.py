from __future__ import annotations

import typing

import flood
from flood import spec

if typing.TYPE_CHECKING:
    import types

    import toolcli


styles: toolcli.StyleTheme = {
    'title': 'bold #00e100',
    'metavar': 'bold #e5e9f0',
    'description': '#aaaaaa',
    'content': '#00B400',
    'option': 'bold #e5e9f0',
    'comment': '#888888',
}


plot_colors = {
    'green_shades': [
        'forestgreen',
        'limegreen',
        'chartreuse',
    ],
    'red_shades': [
        'firebrick',
        'red',
        'salmon',
    ],
    'purple_shades': [
        'rebeccapurple',
        'blueviolet',
        'mediumslateblue',
    ],
    'orange_shades': [
        'darkgoldenrod',
        'darkorange',
        'gold',
    ],
    'blue_shades': [
        'blue',
        'dodgerblue',
        'lightskyblue',
    ],
    'streetlight': [
        'crimson',
        'goldenrod',
        'limegreen',
    ],
}


def get_nodes_plot_colors(
    nodes: typing.Mapping[str, flood.Node]
) -> typing.Mapping[str, str]:
    colors = {}
    taken = set()
    for node in nodes.values():
        # print version
        version = node['client_version']
        if version is None:
            version = ''

        # decide color
        if (
            (version is not None and 'reth' in version)
            or ('reth' in node['name'])
        ) and 'orange_shades' not in taken:
            color = 'orange_shades'
        elif (
            (version is not None and 'erigon' in version)
            or ('erigon' in node['name'])
        ) and 'blue_shades' not in taken:
            color = 'blue_shades'
        else:
            for color_name in plot_colors.keys():
                if color_name not in taken:
                    color = color_name
                    break
            else:
                raise Exception('out of colors')

        colors[node['name']] = color
        taken.add(color)

    return colors


def _get_tqdm() -> types.ModuleType:
    import sys

    if 'jupyter_client' in sys.modules:
        try:
            import ipywidgets  # type: ignore # noqa: F401
            import tqdm.notebook as tqdm

            return tqdm
        except ImportError:
            pass

    import tqdm  # type: ignore

    return tqdm


def print_metric_tables(
    results: typing.Mapping[str, flood.LoadTestOutput],
    metrics: typing.Sequence[str] | None = None,
    suffix: str = '',
    decimals: int = 2,
    comparison: bool = False,
    indent: int = 0,  # Keep for compatibility but ignore
) -> None:
    import toolstr
    
    if metrics is None:
        metrics = ['success', 'throughput', 'p90']
    
    try:
        styles = get_styles()
    except:
        styles = {'metavar': '', 'content': '', 'title': '', 'description': ''}
    
    for metric in metrics:
        # Get labels and data
        labels = list(results.keys())
        if len(labels) == 0:
            continue
            
        # Create column formats
        column_formats = {}
        if comparison and len(results) == 2:
            comparison_label = f'{labels[1]} vs {labels[0]}'
            column_formats[comparison_label] = {
                'decimals': 1,
                'percentage': True,
            }
        
        # Print header - Remove indent parameter
        try:
            toolstr.print_text_box(
                toolstr.add_style(
                    metric + ' vs load' + suffix, styles.get('metavar', '')
                ),
                style=styles.get('content', ''),
            )
        except Exception as e:
            # Fallback to simple print if toolstr fails
            print(f"\n=== {metric} vs load{suffix} ===")
        
        # Get data for this metric
        data = []
        for label in labels:
            result = results[label]
            if hasattr(result, metric):
                values = getattr(result, metric)
                if isinstance(values, list):
                    data.append(values)
                else:
                    data.append([values])
            else:
                data.append([])
        
        # Print the data (simplified version)
        if data:
            print(f"Results for {metric}:")
            for i, label in enumerate(labels):
                if i < len(data) and data[i]:
                    avg_value = sum(data[i]) / len(data[i]) if data[i] else 0
                    print(f"  {label}: {avg_value:.{decimals}f}")
        
        print()  # Add spacing between metrics


#
# # generic restylings of toolstr functions
#


def print_text_box(text: str) -> None:
    import toolstr

    toolstr.print_text_box(
        text,
        text_style=styles.get('metavar'),
        style=styles.get('content'),
    )


def print_header(text: str) -> None:
    import toolstr

    toolstr.print_header(
        text,
        text_style=styles.get('metavar'),
        style=styles.get('content'),
    )


def print_bullet(*args: typing.Any, **kwargs: typing.Any) -> None:
    import toolstr

    toolstr.print_bullet(
        *args,
        **kwargs,
        styles=styles,
    )


def print_table(*args: typing.Any, **kwargs: typing.Any) -> None:
    import toolstr

    toolstr.print_table(
        *args,
        **kwargs,
        label_style=styles.get('metavar'),
        border=styles.get('content'),
    )


def print_multiline_table(*args: typing.Any, **kwargs: typing.Any) -> None:
    import toolstr

    toolstr.print_multiline_table(
        *args,
        **kwargs,
        label_style=styles.get('metavar'),
        border=styles.get('content'),
    )


def print_timestamped(message: str) -> None:
    import datetime
    import toolstr

    dt = datetime.datetime.now()
    if dt.microsecond >= 500_000:
        dt = dt + datetime.timedelta(microseconds=1_000_000 - dt.microsecond)
    else:
        dt = dt - datetime.timedelta(microseconds=dt.microsecond)
    timestamp = (
        toolstr.add_style('\[', styles['content'])
        + toolstr.add_style(str(dt), styles['metavar'])
        + toolstr.add_style(']', styles['content'])
    )
    toolstr.print(timestamp + ' ' + message)


def disable_text_colors() -> None:
    for key in list(styles.keys()):
        del styles[key]  # type: ignore


def get_styles() -> typing.Dict[str, str]:
    """Get styles for output formatting"""
    try:
        # Try to get styles from flood.user_io
        return flood.user_io.styles
    except:
        # Fallback to basic styles if there's an issue
        return {
            'metavar': '',
            'content': '',
            'title': '',
            'description': '',
        }

