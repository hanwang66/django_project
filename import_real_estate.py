import sqlite3
from real_estate.models import RealEstate

def import_real_estate_data():
    conn = sqlite3.connect('real_estate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT community, area, city, floor, price, date FROM real_estate')
    rows = cursor.fetchall()
    for row in rows:
        RealEstate.objects.get_or_create(
            community=row[0],
            area=row[1],
            city=row[2],
            floor=row[3],
            price=row[4],
            date=row[5]
        )
    conn.close()

# 用法：在 Django shell 执行
# from import_real_estate import import_real_estate_data
# import_real_estate_data()
