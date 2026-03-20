from data_base.db import cursor, conn 
from data_base.db import cursor2, conn2

def create_tables():
   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS districts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE)""")

    conn.commit()


    #Тренеры
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coaches(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    addresses TEXT,
    timing TEXT,
    district_id INTEGER,
    FOREIGN KEY(district_id) REFERENCES districts(id))""")

    conn.commit()


def get_trainers_by_district(district_id: int):

    cursor.execute("""
    SELECT MIN(id) as id, name
    FROM coaches
    WHERE district_id = ?
    GROUP BY name """, (district_id,))
    trainers = cursor.fetchall() 

    return trainers

def get_treners_info(trainer_id, district_id):
    cursor.execute("""
    SELECT name, phone, addresses FROM coaches
    WHERE id = ? AND district_id = ?""", (trainer_id, district_id))

    return cursor.fetchall()

def middle_bd():
    trainer_id = 18
    new_name = "Виктория Александровна Голик"

    cursor.execute("""UPDATE coaches SET name = ? WHERE id = ?""", (new_name, trainer_id))
    conn.commit()


def create_table_reservation():
    cursor2.execute("""
    CREATE TABLE IF NOT EXISTS reservation(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_name TEXT,
        phone TEXT,
        child_name TEXT,
        child_age TEXT,
        trainer_name TEXT
    )
    """)
    conn2.commit()

def save_reservation(data: dict):
    try:
        cursor2.execute("""
        INSERT INTO reservation
        (parent_name, phone, child_name, child_age, trainer_name)
        VALUES (?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["phone"],
            data["n_child"],
            data["a_child"],
            data.get("trainer_name", "")
        ))

        conn2.commit()
        print("✅ Данные успешно сохранены:", data)
    except Exception as e:
        print("❌ Ошибка при сохранении в базу:", e)
    