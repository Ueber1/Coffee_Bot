import sqlite3 as sq
from create_bot import bot

def sql_start():
    global base, cur
    base = sq.connect('workers.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS worker(name TEXT, id TEXT PRIMARY KEY)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO worker VALUES (?,?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM worker').fetchall():
        await bot.send_message(message.from_user.id, ret[0]+'-'+ret[1])

async def sql_get_list(list_):
    for ret in cur.execute('SELECT * FROM worker').fetchall():
        list_.append(ret[1])
async def sql_del(id_):
    cur.execute(f'DELETE FROM worker WHERE id = {id_}')