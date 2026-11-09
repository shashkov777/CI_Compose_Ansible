import telebot
import gspread
from google.oauth2.service_account import Credentials
import schedule
import time
import sqlite3

bot = telebot.TeleBot("8573939809:AAE-sW3ZzmUVpCPX-axSO6ryeoyQFWkXaEM")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('cred.json', scopes=scope)
gc = gspread.authorize(creds)


current_row = 1


def mailing():
    global current_row
    sheet = gc.open_by_key('1ZFbBvZjWhSw4MtJL72tfvfZxWTLBpjrqItjEtLgr__w').sheet1 

    msg = sheet.cell(current_row, 2).value

    conn = sqlite3.connect("userfile.db")
    cur = conn.cursor()
    cur.execute("SELECT user_tg_id FROM users WHERE user_tg_id IS NOT NULL")
    for row in cur.fetchall():
        try:
            bot.send_message(row[0], msg)
            time.sleep(0.1)
        except:
            pass
    conn.close()


    current_row += 1

#schedule.every().minute.do(mailing) 
schedule.every().monday.at("11:29").do(mailing)

while True:
    schedule.run_pending()
    time.sleep(60)
