import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('badminton_matches.db')
cursor = conn.cursor()

# Create a table to store match data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        opponent_name TEXT NOT NULL,
        user_score INTEGER NOT NULL,
        opponent_score INTEGER NOT NULL,
        date TEXT NOT NULL,
        remarks TEXT
    )
''')

print("Database and table created successfully.")
conn.close()  # Close the initial connection after creating the table

def insert_match(opponent_name, user_score, opponent_score, date, remarks):
    # Open a new connection for inserting data
    conn = sqlite3.connect('badminton_matches.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Matches (opponent_name, user_score, opponent_score, date, remarks)
        VALUES (?, ?, ?, ?, ?)
    ''', (opponent_name, user_score, opponent_score, date, remarks))
    
    conn.commit()
    print("Match data inserted successfully.")
    conn.close()  # Close the connection after inserting data

# Example usage
insert_match('John Doe', 21, 18, '2024-11-12', 'Good performance with consistent serves.')

def display_all_matches():
    conn = sqlite3.connect('badminton_matches.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Matches')
    rows = cursor.fetchall()
    
    if rows:
        for row in rows:
            print(f"Match ID: {row[0]}, Opponent: {row[1]}, User Score: {row[2]}, Opponent Score: {row[3]}, Date: {row[4]}, Remarks: {row[5]}")
    else:
        print("No matches found.")
    
    conn.close()

# Example usage
display_all_matches()

def calculate_win_loss_ratio():
    conn = sqlite3.connect('badminton_matches.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM Matches WHERE user_score > opponent_score')
    wins = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM Matches WHERE user_score <= opponent_score')
    losses = cursor.fetchone()[0]
    
    if losses == 0:
        print("Win/Loss Ratio: Undefeated!")
    else:
        win_loss_ratio = wins / losses
        print(f"Win/Loss Ratio: {win_loss_ratio:.2f} (Wins: {wins}, Losses: {losses})")
    
    conn.close()

# Example usage
calculate_win_loss_ratio()

def calculate_average_score():
    conn = sqlite3.connect('badminton_matches.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT AVG(user_score) FROM Matches')
    avg_score = cursor.fetchone()[0]
    
    if avg_score is not None:
        print(f"Average User Score: {avg_score:.2f}")
    else:
        print("No matches found.")
    
    conn.close()

# Example usage
calculate_average_score()
