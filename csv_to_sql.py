import csv

# Define the input CSV file and output SQL file
csv_file = "athletics.csv"  # Replace with your CSV file name
sql_file = "output.sql"  # Replace with your desired SQL file name

def create_sql_file(csv_file, sql_file):
    # Create the SQL file and write the SQL commands
    with open(csv_file, "r") as file, open(sql_file, "w") as sql:
        csv_reader = csv.DictReader(file)

        # Write the SQL table creation command
        sql.write('''
        CREATE TABLE IF NOT EXISTS athletes (
            ID INT,
            Name VARCHAR(255),
            Sex VARCHAR(10),
            Age INT,
            Height FLOAT,
            Weight FLOAT,
            Team VARCHAR(255),
            NOC VARCHAR(10),
            Games VARCHAR(255),
            Year INT,
            Season VARCHAR(20),
            City VARCHAR(255),
            Sport VARCHAR(255),
            Event VARCHAR(255),
            Medal VARCHAR(50)
        );
        ''')

        # Generate and write INSERT statements
        for row in csv_reader:
            sql.write("INSERT INTO athletes (ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event, Medal) VALUES (")
            sql.write(
                f"{row['ID']}, '{row['Name'].replace("'", "''")}', '{row['Sex']}', {row['Age']}, {row['Height']}, {row['Weight']}, "
                f"'{row['Team'].replace("'", "''")}', '{row['NOC']}', '{row['Games']}', {row['Year']}, "
                f"'{row['Season']}', '{row['City'].replace("'", "''")}', '{row['Sport'].replace("'", "''")}', "
                f"'{row['Event'].replace("'", "''")}', '{row['Medal'].replace("'", "''")}'"
            )
            sql.write(");\n")

    print(f"SQL file has been successfully created: {sql_file}")

# Run the function
create_sql_file(csv_file, sql_file)
