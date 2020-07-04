"""
This file contains code to load some initial data in to a sqlite3 database

Improvments to be done:
    - Check if there is already data in the tables
    - Check if the structure is the same as the initial datasets
    - DRY principle i.e. code is being repeated, when it shouldn't
"""
import sqlite3
from sqlite3 import Error

# catalog unleashedproductcode initial database data
db_data_catalog_unleashedproductcode = [
    ("GAMEGLI001",  "Incredible Phoenix"),
    ("GAMEGLI002",  "Treasure Gods"),
    ("GAMENSW001",  "Buffalo Bucks"),
    ("GAMENSW002",  "Incredible Phoenix"),
    ("GAMENSW003",  "Gorilla Wins"),
    ("GAMENSW004",  "Lucky Packet"),
    ("GAMENSW005",  "Fortune Lantern 2"),
    ("GAMENSW006",  "Giant's Jackpot"),
    ("GAMENSW007",  "Black Samurai"),
    ("GAMENSW008",  "Chilli Kings"),
    ("GAMENSW009",  "Treasure Stacks"),
    ("GAMENSW010",  "Treasure Gods"),
    ("GAMENSW011",  "Pharaohs Gods"),
    ("GAMENSW012",  "Wu Xing Fa"),
    ("GAMENSW013",  "China League"),
    ("GAMENSW014",  "Acropolis Diamond Pays"),
    ("GAMENSW015",  "Angkor Gold Diamond Pays"),
    ("GAMENSW016",  "Dragon's Gate Diamond Pays"),
    ("GAMENSW017",  "League of Ages"),
    ("GAMENSW018",  "Wild Dragons"),
    ("GAMESAC0026", "Treasure Gods"),
    ("GAMESAC0050", "Pharaohs Gods"),
    ("GAMESAC007",  "Black Samurai"),
    ("GAMESAC029",  "Chilli Kings"),
    ("GAMESAC036",  "Buffalo Bucks"),
    ("GAMESAC045",  "Acropolis Diamond Pays"),
    ("GAMESAC055",  "China League"),
    ("GAMESAC056",  "Angkor Gold Diamond Pays"),
    ("GAMESAC058",  "Dragon's Gate Diamond Pays"),
    ("GAMEVIC0026", "Treasure Gods"),
    ("GAMEVIC0032", "Gorilla Wins"),
    ("GAMEVIC0036", "Buffalo Bucks"),
    ("GAMEVIC0043", "Incredible Phoenix"),
    ("GAMEVIC0045", "Acropolis Diamond Pays"),
    ("GAMEVIC0050", "Pharaohs Gods"),
    ("GAMEVIC0052", "Black Samurai"),
    ("GAMEVIC0056", "Angkor Gold Diamond Pays"),
    ("GAMEVIC0058", "Dragon's Gate Diamond Pays"),
    ("GAMEVIC029",  "Chilli Kings"),
    ("GAMEVIC049",  "Treasure Stacks"),
    ("GAMEVIC055",  "China League"),
    ("EGMA3VIC01",  "Apollo 3 for VIC H&C"),
    ("EGMA3GLI01",  "Apollo 3 for GLI"),
    ("EGMA3NSW01",  "Apollo 3 for NSW (TiTo, no coin)"),
    ("EGMA3NSW01F", "Apollo 3 for NSW (Flat screens, TiTo, no coin)"),
    ("EGMA3NSW02",  "Apollo 3 for NSW (TiTo & coin, no hpper)"),
    ("EGMA3NSW02F", "Apollo 3 for NSW (Flat screens, TiTo & coin, no hpper)"),
    ("EGMA3NSW03",  "Apollo 3 for NSW (BV only)"),
    ("EGMA3NSW03F", "Apollo 3 for NSW (Flat screens, BV only)"),
    ("EGMA3NSW04",  "Apollo 3 for NSW (BV & coin)"),
    ("EGMA3NSW04F", "Apollo 3 for NSW (Flat screens, BV & coin)"),
    ("EGMA3NSW05",  "Apollo 3 for NSW (Everything)"),
    ("EGMA3NSW05F", "Apollo 3 for NSW (Flat screens + everything)"),
    ("EGMA3MEXICO", "Apollo 3 for Mexico"),
    ("EGMA3SAC01",  "Apollo 3 for South Australia"),
    ("EGMA3VIC02",  "Apollo 3 for VIC Casino"),
    ("EGMA3VIC04",  "Apollo 3 for VIC H&C"),
    ("EGMA3VIC05F", "Apollo 3 for VIC H&C (Flat screens & TiTo)"),
    ("EGMA3VIC05",  "Apollo 3 for VIC H&C (TiTo)"),
    ]

db_data_catalog_jurisdictions = [
    ("NSW H&C",    "NSW Clubs & Hotels(BV, Printer, Coin, Hopper)", "63-700"),
    ("NSW H&C",    "NSW Clubs & Hotels(BV, Printer, Coin)","63-701"),
    ("NSW H&C",    "NSW Clubs & Hotels(BV, Printer)", "63-702"),
    ("NSW H&C",    "NSW Clubs & Hotels(BV, Printer, Hopper)", "63-703"),
    ("NSW H&C",    "NSW Clubs & Hotels(BV, Coin)","63-704"),
    ("NSW Casino", "NSW Casino", "63-702"),
    ("VIC H&C",    "Victoria Clubs & Hotels", "63-100"),
    ("VIC Casino", "Crown Casino", "63-400"),
    ("SA H&C",     "South Australia H&C", "63-800"),
    ("SA Casino",  "South Australia Casino (NSW approval)", "63-700"),
    ("NT Casino",  "NT Casino", "63-702"),
    ("ACT H&C",    "ACT Hotels & Clubs", "63-702"),
    ("Mexico",     "Mexico GLI-11", "63-900"),
    ("Peru",       "Peru", "63-600"),
    ("ZA LPM",     "South Africa LPM", "63-200"),
    ("ZA Casinos", "South Africa Casinos", "63-300"),
    ("USA",        "USA GLI-11 (no BV, no printer)", "63-954"),
    ("USA",        "USA with UBA-10 + Epic950", "63-951"),
    ("USA",        "USA with MEI + JCM Gen5", "63-952"),
    ("QLD H&C",    "Queensland Hotels & Clubs", "63-150"),
    ("QLD Casino", "Queensland Casinos", "63-160"),
    ("SA Casino",  "South Australia Casino (QCom based)", "63-150"),
    ("USA",        "USA GLI-11 iVizion + Gen5", "63-950"),
    ("USA",        "USA GLI-11 iVizion + Epic 950", "63-953"),
    ]

db_data_catalog_gamenames = [
    ("Buffalo Bucks",),
    ("Incredible Phoenix",),
    ("Giant's Jackpot",),
    ("Lucky Packet",),
    ("Lucky Packet 2",),
    ("Fortune Lantern",),
    ("Chilli Kings",),
    ("Gorilla Wins",),
    ("Fortune Lantern 2",),
    ("Giant's Jackpot 2",),
    ("Black Samurai",),
    ("Treasure Stacks",),
    ("Treasure Gods",),
    ("Pharaohs Gods",),
    ("Wu Xing Fa",),
    ("China League",),
    ("Acropolis Diamond Pays",),
    ("Angkor Gold Diamond Pays",),
    ("Dragon's Gate Diamond Pays",),
    ("League of Ages",),
    ("Wild Dragons",),
    ("Angkor Gold",),
    ("La Faraona",),
    ("Fiesta De Fantasia",),
    ("Majestic Kingdom",),
    ("Golden Guardian",),
    ("Paititi Gold",),
    ("Golden Mermaid",),
    ("Hawaiian Pearl",),
    ("Angkor Gold Lucky Diamonds",),
    ("Fiesta De Fantasia Lucky Diamonds",),
    ("La Faraona Lucky Diamonds",),
    ("Paititi Gold Lucky Diamonds",),
    ("Lion Wins",),
    ("Lion Wins 2",),
    ("Red Ribbon Double Pack",),
    ("Gold Ribbon",),
    ("Chilli Kings 2",),
    ("Roman Gold II",),
    ("Top Peckins",),
    ("Royal League",),
    ("Enchanted Winnings",),
    ("Angkor Gold 2 Wheel Bonanza",),
    ("Hawaiian Pearl II Wheel Bonanza",),
    ("Golden Mermaid II Wheel Bonanza",),
    ("Red Ribbon Double Pack II",),
    ]


init_data = [
    {
        "data":  db_data_catalog_unleashedproductcode,
        "table_name": "catalog_unleashedproductcode",
        "fieldcodes": ("code","description",),
    },
    {
        "data":  db_data_catalog_jurisdictions,
        "table_name": "catalog_jurisdiction",
        "fieldcodes": ("name", "description", "code",),
    },
    {
        "data":  db_data_catalog_gamenames,
        "table_name": "catalog_gamename",
        "fieldcodes": ("name",),
    },
]


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print(f"Connection to SQLite DB ({path}) successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def add_data(conn, table_data):
    """
    This function adds data to a table in the database
    Only when the table is emtpy will data be written to the database
    :param conn: database connection
    :param table_data: dictionary of table and sql statements to use on the table
    """
    # Default message to return
    ret = f"[WARNING] Data already present in table nothing added to '{table_data['table_name']}'"

    search_code = table_data['fieldcodes'][0]
    search_term = table_data['data'][0][0]

    # Let's build the sql query to check for table content
    exists = f"SELECT count(*) FROM {table_data['table_name']} WHERE {search_code}='{search_term}'"

    # Let's build the sql query to add row entries
    val = table_data['fieldcodes']
    qvl = '?'
    for i in val:
        qvl += ",?"
    qvl = qvl[:-2]
    col = ','.join(table_data['fieldcodes'])

    sql_qry = f"INSERT INTO {table_data['table_name']}({col}) VALUES({qvl})"

    cur = conn.cursor()
    cur.execute(exists)
    count = cur.fetchone()[0] # Check if data is already in the table
    if count == 0:
        cur.executemany(sql_qry, table_data['data'])
        ret = f"[SUCCESS] Data added to the table '{table_data['table_name']}'"

    return ret


if __name__ == '__main__':
    database = "db.sqlite3"
    connection = create_connection(database)

    if connection:
        for table in init_data:
            msg = add_data(connection, table)
            print(msg)
        connection.commit()
        connection.close()
    else:
        print("Failed to open a connection to the database")