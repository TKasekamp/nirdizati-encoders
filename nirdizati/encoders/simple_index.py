import pandas as pd

import encoder


def encode_trace(data, prefix_length=1):
    data_encoder = encoder.Encoder()
    events = data_encoder.get_events(data).tolist()
    cases = data_encoder.get_cases(data)

    columns = []
    columns.append("case_id")
    columns.append("event_nr")
    columns.append("remaining_time")
    columns.append("elapsed_time")
    for i in range(1, prefix_length + 1):
        columns.append("prefix_" + str(i))

    encoded_data = []

    for case in cases:
        df = data[data['case_id'] == case]
        event_length = prefix_length
        case_data = []
        case_data.append(case)
        case_data.append(event_length)
        remaining_time = data_encoder.calculate_remaining_time(df, event_length)
        case_data.append(remaining_time)
        elapsed_time = data_encoder.calculate_elapsed_time(df, event_length)
        case_data.append(elapsed_time)

        case_events = df[df['event_nr'] <= event_length]['activity_name'].tolist()
        for e in case_events:
            case_data.append(events.index(e) + 1)
        encoded_data.append(case_data)

    df = pd.DataFrame(columns=columns, data=encoded_data)
    return df
