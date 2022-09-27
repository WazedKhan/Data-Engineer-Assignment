from fastapi import FastAPI
import sqlite3
import json

app = FastAPI()

DB = "./db.sqlite3"

def get_all_proucts( json_str = False ):
    conn = sqlite3.connect( DB )
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from products
    ''').fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON

    return rows


def get_all_offers( json_str = False ):
    conn = sqlite3.connect( DB )
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from offers
    ''').fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON

    return rows


@app.get("/products")
async def root():
    return {"message": get_all_proucts()}

@app.get("/offers")
async def root():
    return {"message": get_all_offers()}
