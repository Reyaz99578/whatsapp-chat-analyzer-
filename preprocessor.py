import re
import pandas as pd


def preprocess(data):
    # hidden characters hata do
    data = data.replace('\u202f', ' ').replace('\u200e', '').replace('\ufeff', '')

    # line ke start me date-time dhundo (Android + iPhone dono formats)
    pattern = re.compile(
        r'^\[?(\d{1,2}/\d{1,2}/\d{2,4}),?\s(\d{1,2}:\d{2}(?::\d{2})?)\s?([APap][Mm])?\]?\s?-?\s',
        re.MULTILINE
    )

    matches = list(pattern.finditer(data))
    if not matches:
        raise ValueError("Chat me date format match nahi hua. Chat ki pehli 2-3 lines check karo.")

    rows = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(data)
        date_str = m.group(1) + ' ' + m.group(2) + (' ' + m.group(3) if m.group(3) else '')
        rows.append((date_str, data[start:end].strip()))

    df = pd.DataFrame(rows, columns=['date_str', 'user_message'])
    df['date'] = pd.to_datetime(df['date_str'], dayfirst=True, format='mixed', errors='coerce')
    df = df.dropna(subset=['date']).drop(columns=['date_str']).reset_index(drop=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:  # user name mila
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour + 1}")
    df['period'] = period

    return df
