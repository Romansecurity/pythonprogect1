from bs4 import BeautifulSoup
import re
from data_base.db import cursor, conn
import requests

url = "http://tkdvrn.ru/general/raspisanie.php"
response = requests.get(url)
response.encoding = 'cp1251'

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr") 

current_district = None 
last_district = None 

for row in rows: #район 
    district_cell = row.find("td", colspan="5") 
    if district_cell: 
        current_district = district_cell.get_text(strip=True) 
        current_district = " ".join(current_district.split())
        if not current_district:
            continue

        if current_district == last_district: 
            continue 
        last_district = current_district
        

        cursor.execute("""INSERT OR IGNORE INTO districts (name) VALUES (?)""",
                       (current_district,))
        conn.commit() 
        continue
    


  
    current_address = None
    current_address_id = None

    cells_address = row.find_all("td")
    if len(cells_address) > 0 and cells_address[0].has_attr("rowspan"):
        adresses_text = cells_address[0].get_text("\n",strip=True)
        adresses_text = " ".join(adresses_text.split())
        
        current_address = "ул.Машиностроителей, 82 1 этаж. (ост.Пивзавод)"

        cursor.execute(
        """SELECT id FROM coaches WHERE addresses = ?""",
        (current_address,)
        )   
        row_db = cursor.fetchone()
        if row_db:
            current_address_id = row_db[0] 


    if len(cells_address) < 3:
        continue

    coach_text = cells_address[2]

    name_tag = coach_text.find("b")
    if not name_tag:
        continue

    name = name_tag.get_text(" ", strip=True)

    # Телефон через regex
    text = coach_text.get_text()
    phone_match = re.search(r"\+?\d[\d\s()\-]{7,}\d", text)
    phone = phone_match.group() if phone_match else None

    name2 = "Данила Александрович Хрыпченко"
    phone2 = "8(950)752-35-28"
    row_id = 329

    cursor.execute("""
    UPDATE coaches
    SET name = ?, phone = ?
    WHERE id = ?
""", (name2, phone2, row_id))



    conn.commit()


    


    
        







    

    
    


    










        
        

    


