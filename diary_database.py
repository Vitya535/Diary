import sqlite3

conn = sqlite3.connect("data_for_diary.db")  # создание связи с базой данных

cursor = conn.cursor()
cursor.execute('''CREATE TABLE diary_events
                (event_title text, event_time text)''')
# создание таблицы: event_title - название события, event_time - время события
conn.close()
# сделать чтобы эти записи отображались на ежедневнике
