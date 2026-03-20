from data_base.db import cursor, conn 

def middle_bd():
    cursor.execute("""
        UPDATE coaches
        SET addresses == addresses || '\nМБОУ СОШ №4 бул. Пионеров, 14'
        WHERE id = 15""")
    conn.commit()