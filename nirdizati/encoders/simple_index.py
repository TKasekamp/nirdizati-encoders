import pandas as pd

from nirdizati.encoders.helper import *


def encode_trace(data, prefix_length=1, next_activity=False):
    if next_activity:
        return __encode_next_activity(data, prefix_length)
    else:
        return __encode_simple(data, prefix_length)


def __encode_simple(data, prefix_length):
    events = get_events(data).tolist()
    cases = get_cases(data)

    columns = __create_columns(prefix_length)
    encoded_data = []

    for case in cases:
        df = data[data['case_id'] == case]
        event_length = prefix_length
        case_data = []
        case_data.append(case)
        case_data.append(event_length)
        remaining_time = calculate_remaining_time(df, event_length)
        case_data.append(remaining_time)
        elapsed_time = calculate_elapsed_time(df, event_length)
        case_data.append(elapsed_time)

        case_events = df[df['event_nr'] <= event_length]['activity_name'].tolist()
        for e in case_events:
            case_data.append(events.index(e) + 1)
        encoded_data.append(case_data)

    df = pd.DataFrame(columns=columns, data=encoded_data)
    return df


def __encode_next_activity(data, prefix_length):
    events = get_events(data).tolist()
    cases = get_cases(data)

    max_length = max(data['event_nr'])
    columns = __columns_next_activity(max_length)

    encoded_data = []

    for case in cases:
        df = data[data['case_id'] == case]
        for event_length in range(1, max(df['event_nr'])):
            case_data = []
            case_data.append(case)
            case_data.append(event_length)

            case_events = df[df['event_nr'] <= event_length]['activity_name'].tolist()
            # all but last
            for e in case_events[:-1]:
                case_data.append(events.index(e) + 1)

            for k in range(len(case_events), max_length):
                case_data.append(0)

            # last is label
            label = events.index(case_events[-1]) + 1
            case_data.append(label)
            encoded_data.append(case_data)

    df = pd.DataFrame(columns=columns, data=encoded_data)
    return df


def __create_columns(prefix_length):
    columns = list(DEFAULT_COLUMNS)
    for i in range(1, prefix_length + 1):
        columns.append("prefix_" + str(i))
    return columns


def __columns_next_activity(max_length):
    """Creates columns for next activity"""
    columns = ["case_id", "event_nr"]
    for i in range(1, max_length):
        columns.append("prefix_" + str(i))
    columns.append("label")
    return columns
