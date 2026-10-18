import os
from collections import Counter

import emoji
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()


def _filter_user(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df


def _load_stop_words():
    # stop_hinglish.txt isi folder me rakho (optional)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stop_hinglish.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return set(f.read().split())
    return set()


def _clean_messages(selected_user, df):
    df = _filter_user(selected_user, df)
    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', regex=False)]
    temp = temp[~temp['message'].str.contains('This message was deleted', regex=False)]
    return temp.copy()


def fetch_stats(selected_user, df):
    df = _filter_user(selected_user, df)

    # number of messages
    num_messages = df.shape[0]

    # total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # media messages
    num_media_messages = df[df['message'].str.contains('<Media omitted>', regex=False)].shape[0]

    # links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    percent_df.columns = ['name', 'percent']
    return x, percent_df


def create_wordcloud(selected_user, df):
    stop_words = _load_stop_words()
    temp = _clean_messages(selected_user, df)

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message'] = temp['message'].apply(remove_stop_words)
    text = temp['message'].str.cat(sep=" ")
    if text.strip() == "":
        text = "no words"

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(text)


def most_common_words(selected_user, df):
    stop_words = _load_stop_words()
    temp = _clean_messages(selected_user, df)

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user, df):
    df = _filter_user(selected_user, df)

    emojis = []
    for message in df['message']:
        emojis.extend([e['emoji'] for e in emoji.emoji_list(message)])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user, df):
    df = _filter_user(selected_user, df)

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    df = _filter_user(selected_user, df)
    return df.groupby('only_date').count()['message'].reset_index()


def week_activity_map(selected_user, df):
    df = _filter_user(selected_user, df)
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    df = _filter_user(selected_user, df)
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    df = _filter_user(selected_user, df)
    return df.pivot_table(
        index='day_name', columns='period', values='message', aggfunc='count'
    ).fillna(0)
