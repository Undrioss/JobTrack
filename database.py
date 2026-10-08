
import sqlite3


class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("jobtrack.db")
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                location TEXT,
                salary TEXT,
                status TEXT NOT NULL,
                date_applied TEXT NOT NULL,
                notes TEXT
            )
        """)
        self.connection.commit()

    def add_application(self, company, position, location,
                        salary, status, date_applied, notes):

        self.connection.execute("""
            INSERT INTO applications (
                company,
                position,
                location,
                salary,
                status,
                date_applied,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            company,
            position,
            location,
            salary,
            status,
            date_applied,
            notes
        ))

        self.connection.commit()
        print("Job application saved successfully!")

    def get_applications(self):
        cursor = self.connection.execute("""
            SELECT *
            FROM applications
            ORDER BY date_applied DESC
        """)

        return cursor.fetchall()

    def update_application(self, application_id, new_status):
        cursor = self.connection.execute("""
            UPDATE applications
            SET status = ?
            WHERE id = ?
        """, (new_status, application_id))

        self.connection.commit()

        if cursor.rowcount > 0:
            print("Application updated successfully!")
        else:
            print("No application found with that ID.")

    def delete_application(self, application_id):
        cursor = self.connection.execute("""
            DELETE FROM applications
            WHERE id = ?
        """, (application_id,))

        self.connection.commit()

        if cursor.rowcount > 0:
            print("Application deleted successfully!")
        else:
            print("No application found with that ID.")

    def close(self):
        self.connection.close()
