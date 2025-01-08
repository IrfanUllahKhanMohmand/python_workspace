import sqlite3
import csv

# Define the input CSV file and SQLite database file
csv_file = "athletics.csv"  # Replace with your CSV file name
db_file = "normalized_output.db"  # Replace with your desired SQLite database file name

def create_normalized_database(csv_file, db_file):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables based on the normalized schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Athletes (
            AthleteID INTEGER PRIMARY KEY,
            Name TEXT,
            Sex TEXT,
            Age INTEGER,
            Height REAL,
            Weight REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teams (
            TeamID INTEGER PRIMARY KEY,
            TeamName TEXT,
            NOC TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            GameID INTEGER PRIMARY KEY,
            Games TEXT,
            Year INTEGER,
            Season TEXT,
            City TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sports (
            SportID INTEGER PRIMARY KEY,
            Sport TEXT,
            Event TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Medals (
            MedalID INTEGER PRIMARY KEY,
            AthleteID INTEGER,
            GameID INTEGER,
            SportID INTEGER,
            TeamID INTEGER,
            Medal TEXT,
            FOREIGN KEY (AthleteID) REFERENCES Athletes (AthleteID),
            FOREIGN KEY (GameID) REFERENCES Games (GameID),
            FOREIGN KEY (SportID) REFERENCES Sports (SportID),
            FOREIGN KEY (TeamID) REFERENCES Teams (TeamID)
        )
    ''')

    # Dictionaries to store unique entries for Teams, Games, and Sports
    teams = {}
    games = {}
    sports = {}
    processed_athletes = set()  # Use a set to track processed AthleteIDs

    # Read the CSV file and process the data
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Insert into Athletes table (only if the AthleteID is not already processed)
            athlete_id = row["ID"]
            if athlete_id not in processed_athletes:
                cursor.execute('''
                    INSERT INTO Athletes (AthleteID, Name, Sex, Age, Height, Weight)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (athlete_id, row["Name"], row["Sex"], row["Age"], row["Height"], row["Weight"]))
                processed_athletes.add(athlete_id)

            # Insert into Teams table
            team_key = (row["Team"], row["NOC"])
            if team_key not in teams:
                cursor.execute('''
                    INSERT INTO Teams (TeamName, NOC)
                    VALUES (?, ?)
                ''', team_key)
                teams[team_key] = cursor.lastrowid

            # Insert into Games table
            game_key = (row["Games"], row["Year"], row["Season"], row["City"])
            if game_key not in games:
                cursor.execute('''
                    INSERT INTO Games (Games, Year, Season, City)
                    VALUES (?, ?, ?, ?)
                ''', game_key)
                games[game_key] = cursor.lastrowid

            # Insert into Sports table
            sport_key = (row["Sport"], row["Event"])
            if sport_key not in sports:
                cursor.execute('''
                    INSERT INTO Sports (Sport, Event)
                    VALUES (?, ?)
                ''', sport_key)
                sports[sport_key] = cursor.lastrowid

            # Insert into Medals table
            cursor.execute('''
                INSERT INTO Medals (AthleteID, GameID, SportID, TeamID, Medal)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                athlete_id,
                games[game_key],
                sports[sport_key],
                teams[team_key],
                row["Medal"]
            ))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Data has been successfully imported into the normalized database: {db_file}")

# Run the function
create_normalized_database(csv_file, db_file)
