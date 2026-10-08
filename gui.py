
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import DatabaseManager

import csv
from tkinter import filedialog


class JobTrackGUI:

    def __init__(self, root):
        self.root = root
        self.db = DatabaseManager()

        self.root.title("JobTrack - Application Manager")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)
        self.root.configure(bg="#f1f5f9")

        self.create_interface()
        self.load_applications()

        # Close database properly when exiting
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_interface(self):
        # Main header
        header = tk.Frame(
            self.root,
            bg="#2563eb",
            height=80
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="JobTrack",
            font=("Segoe UI", 26, "bold"),
            fg="white",
            bg="#2563eb"
        )
        title.pack(side="left", padx=30, pady=18)

        # Main content area
        content = ttk.Frame(
            self.root,
            padding=25
        )
        content.pack(fill="both", expand=True)

        welcome = ttk.Label(
            content,
            text="Job Application Dashboard",
            font=("Segoe UI", 20, "bold")
        )
        welcome.pack(anchor="w", pady=(0, 20))

        description = ttk.Label(
            content,
            text="Manage and track your job applications in one place.",
            font=("Segoe UI", 11)
        )
        description.pack(anchor="w")

        # Dashboard statistics
        stats_frame = ttk.Frame(content)
        stats_frame.pack(fill="x", pady=(20, 0))

        self.stat_labels = {}

        stats = [
            "Total Applications",
            "Applied",
            "Interviews",
            "Offers",
            "Rejected"
        ]

        for index, name in enumerate(stats):
            card = tk.Frame(
                stats_frame,
                bg="white",
                highlightbackground="#cbd5e1",
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                padx=5,
                sticky="nsew"
            )

            stats_frame.columnconfigure(index, weight=1)

            tk.Label(
                card,
                text=name,
                bg="white",
                font=("Segoe UI", 10)
            ).pack(pady=(12, 4))

            value_label = tk.Label(
                card,
                text="0",
                bg="white",
                fg="#2563eb",
                font=("Segoe UI", 22, "bold")
            )
            value_label.pack(pady=(0, 12))

            self.stat_labels[name] = value_label

        # Button section
        button_frame = ttk.Frame(content)
        button_frame.pack(fill="x", pady=(20, 0))

        add_button = ttk.Button(
            button_frame,
            text="+ Add Application",
            command=self.open_add_window
        )
        add_button.pack(side="left", padx=(0, 10))

        edit_button = ttk.Button(
            button_frame,
            text="Edit Selected",
            command=self.edit_selected_application
        )
        edit_button.pack(side="left", padx=(0, 10))

        delete_button = ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_selected_application
        )
        delete_button.pack(side="left")

        export_button = ttk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_to_csv
        )
        export_button.pack(side="left", padx=(10, 0))

        # Search section
        search_frame = ttk.Frame(content)
        search_frame.pack(fill="x", pady=(20, 0))

        search_label = ttk.Label(
            search_frame,
            text="Search Applications:"
        )
        search_label.pack(side="left", padx=(0, 10))

        self.search_var = tk.StringVar()

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )
        search_entry.pack(side="left")

        # Update results while typing
        self.search_var.trace_add(
            "write",
            lambda *args: self.load_applications()
        )

        # Job applications table
        table_frame = ttk.Frame(content)
        table_frame.pack(
            fill="both",
            expand=True,
            pady=(25, 0)
        )

        columns = (
            "id",
            "company",
            "position",
            "location",
            "salary",
            "status",
            "date"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "id": "ID",
            "company": "Company",
            "position": "Position",
            "location": "Location",
            "salary": "Salary",
            "status": "Status",
            "date": "Date Applied"
        }

        for column in columns:
            self.table.heading(
                column,
                text=headings[column]
            )

            self.table.column(
                column,
                width=70 if column == "id" else 140,
                minwidth=60,
                stretch=(column != "id")
            )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")

    # ------------------------------------------
    # ADD APPLICATION WINDOW
    # ------------------------------------------

    def open_add_window(self):
        add_window = tk.Toplevel(self.root)

        add_window.title("Add New Job Application")
        add_window.geometry("450x650")
        add_window.resizable(False, False)
        add_window.transient(self.root)
        add_window.grab_set()

        title = ttk.Label(
            add_window,
            text="New Job Application",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)

        form_frame = ttk.Frame(
            add_window,
            padding=20
        )
        form_frame.pack(fill="both", expand=True)

        # Store form inputs
        entries = {}

        fields = [
            ("Company", "company"),
            ("Position", "position"),
            ("Location", "location"),
            ("Salary", "salary"),
            ("Date Applied (YYYY-MM-DD)", "date")
        ]

        for label_text, field_name in fields:
            label = ttk.Label(
                form_frame,
                text=label_text
            )
            label.pack(anchor="w", pady=(8, 2))

            entry = ttk.Entry(
                form_frame,
                width=40
            )
            entry.pack(fill="x")

            entries[field_name] = entry

        # Automatically fill today's date
        entries["date"].insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # Status dropdown
        status_label = ttk.Label(
            form_frame,
            text="Application Status"
        )
        status_label.pack(anchor="w", pady=(8, 2))

        status_var = tk.StringVar(value="Applied")

        status_dropdown = ttk.Combobox(
            form_frame,
            textvariable=status_var,
            values=[
                "Applied",
                "Interview",
                "Offer",
                "Rejected"
            ],
            state="readonly"
        )
        status_dropdown.pack(fill="x")

        # Notes
        notes_label = ttk.Label(
            form_frame,
            text="Notes"
        )
        notes_label.pack(anchor="w", pady=(8, 2))

        notes_input = tk.Text(
            form_frame,
            height=4,
            width=40
        )
        notes_input.pack(fill="x")

        # Save button
        save_button = ttk.Button(
            form_frame,
            text="Save Application",
            command=lambda: self.save_application(
                add_window,
                entries,
                status_var,
                notes_input
            )
        )
        save_button.pack(pady=20)

    # ------------------------------------------
    # SAVE APPLICATION
    # ------------------------------------------

    def save_application(
            self, window, entries, status_var, notes_input
    ):
        # Collect information
        company = entries["company"].get().strip()
        position = entries["position"].get().strip()
        location = entries["location"].get().strip()
        salary = entries["salary"].get().strip()
        date_applied = entries["date"].get().strip()
        status = status_var.get()
        notes = notes_input.get("1.0", tk.END).strip()

        # Validate required fields
        if not company or not position or not date_applied:
            messagebox.showerror(
                "Missing Information",
                "Company, Position and Date Applied are required.",
                parent=window
            )
            return

        # Validate date format
        try:
            parsed_date = datetime.strptime(
                date_applied,
                "%Y-%m-%d"
            )

            if parsed_date.strftime("%Y-%m-%d") != date_applied:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please enter the date as YYYY-MM-DD.",
                parent=window
            )
            return

        # Save to SQLite database
        try:
            self.db.add_application(
                company=company,
                position=position,
                location=location,
                salary=salary,
                status=status,
                date_applied=date_applied,
                notes=notes
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not save application:\n{error}",
                parent=window
            )
            return

        # Refresh applications table
        self.load_applications()

        # Close form
        window.destroy()

        messagebox.showinfo(
            "Success",
            "Job application saved successfully!",
            parent=self.root
        )

    # ------------------------------------------
    # EDIT APPLICATION
    # ------------------------------------------

    def edit_selected_application(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an application to edit."
            )
            return

        item = self.table.item(selected[0])

        application_id = item["values"][0]
        company = item["values"][1]
        current_status = item["values"][5]

        edit_window = tk.Toplevel(self.root)

        edit_window.title("Edit Application")
        edit_window.geometry("400x280")
        edit_window.resizable(False, False)
        edit_window.transient(self.root)
        edit_window.grab_set()

        ttk.Label(
            edit_window,
            text=f"Edit {company}",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        ttk.Label(
            edit_window,
            text="Application Status"
        ).pack(pady=(10, 5))

        status_var = tk.StringVar(value=current_status)

        status_dropdown = ttk.Combobox(
            edit_window,
            textvariable=status_var,
            values=[
                "Applied",
                "Interview",
                "Offer",
                "Rejected"
            ],
            state="readonly",
            width=30
        )
        status_dropdown.pack(pady=5)

        def save_changes():
            new_status = status_var.get()

            try:
                self.db.update_application(
                    application_id,
                    new_status
                )

            except Exception as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not update application:\n{error}",
                    parent=edit_window
                )
                return

            self.load_applications()
            edit_window.destroy()

            messagebox.showinfo(
                "Success",
                "Application updated successfully!",
                parent=self.root
            )

        ttk.Button(
            edit_window,
            text="Save Changes",
            command=save_changes
        ).pack(pady=25)

    # ------------------------------------------
    # DELETE APPLICATION
    # ------------------------------------------

    def delete_selected_application(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an application first."
            )
            return

        item = self.table.item(selected[0])

        application_id = item["values"][0]
        company = item["values"][1]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete "
            f"the application for {company}?",
            parent=self.root
        )

        if not confirm:
            return

        try:
            self.db.delete_application(application_id)

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete application:\n{error}",
                parent=self.root
            )
            return

        self.load_applications()

        messagebox.showinfo(
            "Deleted",
            "Application deleted successfully!",
            parent=self.root
        )

    # ------------------------------------------
    # LOAD AND SEARCH APPLICATIONS
    # ------------------------------------------

    def export_to_csv(self):
        # Get all applications from the database
        applications = self.db.get_applications()

        if not applications:
            messagebox.showwarning(
                "No Data",
                "There are no applications to export."
            )
            return

        # Ask the user where to save the file
        file_path = filedialog.asksaveasfilename(
            title="Export Job Applications",
            defaultextension=".csv",
            initialfile="job_applications.csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        # Stop if the user cancels
        if not file_path:
            return

        # Define the CSV column headings
        columns = [
            "id",
            "company",
            "position",
            "location",
            "salary",
            "status",
            "date_applied",
            "notes"
        ]

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:
                writer = csv.writer(file)

                writer.writerow([
                    "ID",
                    "Company",
                    "Position",
                    "Location",
                    "Salary",
                    "Status",
                    "Date Applied",
                    "Notes"
                ])

                for application in applications:
                    writer.writerow([
                        application[column]
                        for column in columns
                    ])

            messagebox.showinfo(
                "Export Successful",
                f"Successfully exported "
                f"{len(applications)} applications!"
            )

        except OSError as error:
            messagebox.showerror(
                "Export Failed",
                f"Could not export applications:\n{error}"
            )

    def update_statistics(self):
        applications = self.db.get_applications()

        counts = {
            "Total Applications": len(applications),
            "Applied": 0,
            "Interviews": 0,
            "Offers": 0,
            "Rejected": 0
        }

        status_mapping = {
            "Applied": "Applied",
            "Interview": "Interviews",
            "Offer": "Offers",
            "Rejected": "Rejected"
        }

        for application in applications:
            status = application["status"]
            label = status_mapping.get(status)

            if label:
                counts[label] += 1

        for name, label in self.stat_labels.items():
            label.config(text=str(counts[name]))

    def load_applications(self):
        # Clear current rows
        for item in self.table.get_children():
            self.table.delete(item)

        # Retrieve applications from database
        applications = self.db.get_applications()

        # Refresh dashboard counters
        self.update_statistics()

        # Get search query
        search_text = self.search_var.get().strip().lower()

        # Display matching applications
        for application in applications:
            company = (application["company"] or "").lower()
            position = (application["position"] or "").lower()
            location = (application["location"] or "").lower()

            if search_text:
                if not (
                    search_text in company
                    or search_text in position
                    or search_text in location
                ):
                    continue

            self.table.insert(
                "",
                "end",
                values=(
                    application["id"],
                    application["company"],
                    application["position"],
                    application["location"],
                    application["salary"],
                    application["status"],
                    application["date_applied"]
                )
            )

    # ------------------------------------------
    # CLOSE APPLICATION
    # ------------------------------------------

    def on_close(self):
        self.db.close()
        self.root.destroy()


# ----------------------------------------------
# APPLICATION ENTRY POINT
# ----------------------------------------------

def start_gui():
    root = tk.Tk()
    JobTrackGUI(root)
    root.mainloop()
