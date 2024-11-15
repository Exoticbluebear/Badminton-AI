import sqlite3
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout,
                             QLineEdit, QPushButton, QTextEdit, QMessageBox, QLabel)

class BadmintonMatchTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Badminton Match Tracker')
        self.setGeometry(100, 100, 400, 400)

        # Layouts
        form_layout = QFormLayout()
        main_layout = QVBoxLayout()

        # Input Fields
        self.entry_opponent = QLineEdit()
        self.entry_user_score = QLineEdit()
        self.entry_opponent_score = QLineEdit()
        self.entry_date = QLineEdit()
        self.entry_remarks = QLineEdit()

        form_layout.addRow('Opponent Name:', self.entry_opponent)
        form_layout.addRow('User Score:', self.entry_user_score)
        form_layout.addRow('Opponent Score:', self.entry_opponent_score)
        form_layout.addRow('Date (YYYY-MM-DD):', self.entry_date)
        form_layout.addRow('Remarks:', self.entry_remarks)

        # Buttons
        self.insert_button = QPushButton('Insert Match')
        self.insert_button.clicked.connect(self.insert_match)
        self.display_button = QPushButton('Display All Matches')
        self.display_button.clicked.connect(self.display_all_matches)
        self.displayRatio_button = QPushButton('Display Win/Loss ratio')
        self.displayRatio_button.clicked.connect(self.calculate_win_loss_ratio)

        # Text display
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)

        # Add widgets to main layout
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.insert_button)
        main_layout.addWidget(self.display_button)
        main_layout.addWidget(self.displayRatio_button)
        main_layout.addWidget(self.display_text)

        self.setLayout(main_layout)

    def insert_match(self):
        opponent_name = self.entry_opponent.text()
        user_score = self.entry_user_score.text()
        opponent_score = self.entry_opponent_score.text()
        date = self.entry_date.text()
        remarks = self.entry_remarks.text()

        # Validate input fields
        if not opponent_name or not user_score or not opponent_score or not date:
            QMessageBox.critical(self, 'Error', 'Please fill in all fields.')
            return

        try:
            user_score = int(user_score)
            opponent_score = int(opponent_score)
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Scores must be numeric.')
            return

        # Database operations
        conn = sqlite3.connect('badminton_matches.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Matches (opponent_name, user_score, opponent_score, date, remarks)
            VALUES (?, ?, ?, ?, ?)
        ''', (opponent_name, user_score, opponent_score, date, remarks))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Success', 'Match data inserted successfully.')
        self.clear_entries()

    def display_all_matches(self):
        conn = sqlite3.connect('badminton_matches.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Matches')
        rows = cursor.fetchall()
        conn.close()

        self.display_text.clear()
        if rows:
            for row in rows:
                self.display_text.append(f"Match ID: {row[0]}, Opponent: {row[1]}, User Score: {row[2]}, "
                                         f"Opponent Score: {row[3]}, Date: {row[4]}, Remarks: {row[5]}")
        else:
            self.display_text.append("No matches found.")
    
    def calculate_win_loss_ratio(self):
        conn = sqlite3.connect('badminton_matches.db')
        cursor = conn.cursor()
    
        cursor.execute('SELECT COUNT(*) FROM Matches WHERE user_score > opponent_score')
        wins = cursor.fetchone()[0]
    
        cursor.execute('SELECT COUNT(*) FROM Matches WHERE user_score <= opponent_score')
        losses = cursor.fetchone()[0]
    
        if losses == 0:
          self.display_text.append("Win/Loss Ratio: Undefeated!")
        else:
          win_loss_ratio = wins / losses
        self.display_text.append(f"Win/Loss Ratio: {win_loss_ratio:.2f} (Wins: {wins}, Losses: {losses})")
    
        conn.close()

    def clear_entries(self):
        self.entry_opponent.clear()
        self.entry_user_score.clear()
        self.entry_opponent_score.clear()
        self.entry_date.clear()
        self.entry_remarks.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BadmintonMatchTracker()
    window.show()
    sys.exit(app.exec_())
