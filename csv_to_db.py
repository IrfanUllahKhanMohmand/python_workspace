import sqlite3
import csv

# Define the input CSV file and SQLite database file
csv_file = "athletics.csv"  # Replace with your CSV file name
db_file = "output.db"    # Replace with your desired SQLite database file name

def create_database(csv_file, db_file):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS athletes (
            ID INTEGER,
            Name TEXT,
            Sex TEXT,
            Age INTEGER,
            Height REAL,
            Weight REAL,
            Team TEXT,
            NOC TEXT,
            Games TEXT,
            Year INTEGER,
            Season TEXT,
            City TEXT,
            Sport TEXT,
            Event TEXT,
            Medal TEXT
        )
    ''')

    # Read the CSV file and insert the data into the table
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        rows = [
            (
                row["ID"], row["Name"], row["Sex"], row["Age"], row["Height"],
                row["Weight"], row["Team"], row["NOC"], row["Games"], row["Year"],
                row["Season"], row["City"], row["Sport"], row["Event"], row["Medal"]
            ) for row in csv_reader
        ]

    # Insert data into the database
    cursor.executemany('''
        INSERT INTO athletes (ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event, Medal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', rows)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Data has been successfully imported into {db_file}")

# Run the function
create_database(csv_file, db_file)
