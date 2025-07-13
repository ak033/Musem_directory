import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import mysql.connector
from mysql.connector import Error
import time

class MuseumDatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Museum Database Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection variables
        self.cxn = None
        self.cur = None
        self.current_user_role = None
        
        # Table definitions
        self.tables = {
            "ART_OBJECT": ["ID_NO", "ARTIST_NAME", "OBJECT_YEAR", "TITLE", "ORIGIN", "DECRIPTION", "EPOCH"],
            "ARTIST": ["ARTIST_NAME", "DATE_BORN", "DATE_DIED", "COUNTRY_ORIGIN", "EPOCH", "MAIN_STYLE", "DESCRIPTION"],
            "BORROWED": ["BORROWED_ID", "NAME_OF_COLLECTION", "DATE_BORROWED", "DATE_RETURNED"],
            "COLLECTIONS": ["COLLECTION_NAME", "COLLECTION_TYPE", "COLLECTION_DESCRIPTION", "ADDRESS", "PHONE", "CONTACT_PERSON"],
            "EXHIBITIONS": ["EXHIBITION_NAME", "START_DATE", "END_DATE"],
            "OTHER": ["OTHER_ID", "TYPE_ART", "STYLE"],
            "PAINTING": ["PAINTING_ID", "PAINT_TYPE", "DRAW_ON", "STYLE"],
            "PERMANENT_COLLECTIONS": ["PC_ID", "DATE_AQQUIRED", "PC_STATUS", "COST"],
            "SCULPTURE": ["STRUCTURE_ID", "MATERIAL", "HEIGHT", "WEIGHT", "STYLE"],
            "DISPLAYS": ["OBJECT_NUM", "EXHIBITION_NAME"],
        }
        
        self.parent_tables = ["ARTIST", "ARTOBJECT", "COLLECTION", "EXHIBITION"]
        self.illegal_columns = ["ARTISTNAME", "IDNUM", "COLLECTIONNAME", "EXBNNAME", "OBJECTIDNUM"]
        
        self.create_login_screen()
    
    def create_login_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Museum Database Management System", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=30)
        
        # Login frame
        login_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        login_frame.pack(pady=20, padx=100, fill='x')
        
        tk.Label(login_frame, text="Please select your role:", 
                font=('Arial', 14), bg='#ffffff').pack(pady=20)
        
        # Role selection
        self.role_var = tk.StringVar(value="3")
        roles = [("Admin", "1"), ("Employee", "2"), ("Guest", "3")]
        
        for text, value in roles:
            tk.Radiobutton(login_frame, text=text, variable=self.role_var, value=value,
                          font=('Arial', 12), bg='#ffffff').pack(pady=5)
        
        # Username and password fields
        cred_frame = tk.Frame(login_frame, bg='#ffffff')
        cred_frame.pack(pady=20)
        
        tk.Label(cred_frame, text="Username:", font=('Arial', 12), bg='#ffffff').grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = tk.Entry(cred_frame, font=('Arial', 12), width=20)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(cred_frame, text="Password:", font=('Arial', 12), bg='#ffffff').grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = tk.Entry(cred_frame, font=('Arial', 12), width=20, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Login button
        login_btn = tk.Button(login_frame, text="Login", font=('Arial', 12, 'bold'),
                             bg='#3498db', fg='white', command=self.login)
        login_btn.pack(pady=20)
        
        # Guest note
        note_label = tk.Label(login_frame, text="Note: Guest users don't need credentials", 
                             font=('Arial', 10), bg='#ffffff', fg='#7f8c8d')
        note_label.pack(pady=10)
    
    def login(self):
        role = self.role_var.get()
        username = self.username_entry.get() if role in ['1', '2'] else "guest"
        password = self.password_entry.get() if role in ['1', '2'] else None
        
        try:
            self.cxn = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                database="MUSEUM",
                user=username,
                password=password
            )
            self.cur = self.cxn.cursor()
            self.current_user_role = role
            
            # Create main application interface
            if role == '1':
                self.create_admin_interface()
            elif role == '2':
                self.create_employee_interface()
            else:
                self.create_guest_interface()
                
        except Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
    
    def create_admin_interface(self):
        self.clear_window()
        
        # Title
        title_label = tk.Label(self.root, text="Admin Dashboard", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#e74c3c')
        title_label.pack(pady=20)
        
        # Button frame
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        # SQL Command button
        sql_btn = tk.Button(btn_frame, text="Execute SQL Command", 
                           font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.execute_sql_command)
        sql_btn.pack(pady=10, padx=20, fill='x')
        
        # Run SQL Script button
        script_btn = tk.Button(btn_frame, text="Run SQL Script from File", 
                              font=('Arial', 12), bg='#e74c3c', fg='white',
                              command=self.run_sql_script)
        script_btn.pack(pady=10, padx=20, fill='x')
        
        # Logout button
        logout_btn = tk.Button(btn_frame, text="Logout", 
                              font=('Arial', 12), bg='#95a5a6', fg='white',
                              command=self.logout)
        logout_btn.pack(pady=10, padx=20, fill='x')
        
        # Results area
        self.create_results_area()
    
    def create_employee_interface(self):
        self.clear_window()
        
        # Title
        title_label = tk.Label(self.root, text="Employee Dashboard", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2ecc71')
        title_label.pack(pady=20)
        
        # Button frame
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        buttons = [
            ("Lookup Information", self.lookup_info),
            ("Insert Data", self.insert_data),
            ("Update Data", self.update_data),
            ("Delete Data", self.delete_data),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            color = '#95a5a6' if text == 'Logout' else '#2ecc71'
            btn = tk.Button(btn_frame, text=text, font=('Arial', 12), 
                           bg=color, fg='white', command=command)
            btn.pack(pady=5, padx=20, fill='x')
        
        # Results area
        self.create_results_area()
    
    def create_guest_interface(self):
        self.clear_window()
        
        # Title
        title_label = tk.Label(self.root, text="Guest View", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#9b59b6')
        title_label.pack(pady=20)
        
        # Table selection frame
        table_frame = tk.Frame(self.root, bg='#f0f0f0')
        table_frame.pack(pady=20)
        
        tk.Label(table_frame, text="Select a table to view:", 
                font=('Arial', 14), bg='#f0f0f0').pack(pady=10)
        
        # Get table names
        self.cur.execute("SHOW TABLES")
        tables = [row[0] for row in self.cur.fetchall()]
        
        self.table_var = tk.StringVar()
        table_combo = ttk.Combobox(table_frame, textvariable=self.table_var, 
                                  values=tables, font=('Arial', 12))
        table_combo.pack(pady=10)
        
        # View button
        view_btn = tk.Button(table_frame, text="View Table", 
                            font=('Arial', 12), bg='#9b59b6', fg='white',
                            command=self.view_table_guest)
        view_btn.pack(pady=10)
        
        # Logout button
        logout_btn = tk.Button(table_frame, text="Logout", 
                              font=('Arial', 12), bg='#95a5a6', fg='white',
                              command=self.logout)
        logout_btn.pack(pady=10)
        
        # Results area
        self.create_results_area()
    
    def create_results_area(self):
        # Results frame
        results_frame = tk.Frame(self.root, bg='#f0f0f0')
        results_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Treeview for results
        self.tree = ttk.Treeview(results_frame)
        self.tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.tree.yview)
        v_scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(self.root, orient='horizontal', command=self.tree.xview)
        h_scrollbar.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=h_scrollbar.set)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def execute_sql_command(self):
        sql_command = simpledialog.askstring("SQL Command", "Enter your SQL command:")
        if sql_command:
            try:
                self.cur.execute(sql_command)
                if sql_command.strip().upper().startswith('SELECT'):
                    self.display_results()
                else:
                    self.cxn.commit()
                    messagebox.showinfo("Success", "Command executed successfully")
            except Error as e:
                messagebox.showerror("SQL Error", f"Error executing command: {e}")
    
    def run_sql_script(self):
        file_path = filedialog.askopenfilename(
            title="Select SQL Script File",
            filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    sql_script = file.read()
                
                commands = sql_script.split(';')
                success_count = 0
                
                for command in commands:
                    command = command.strip()
                    if command:
                        try:
                            self.cur.execute(command)
                            success_count += 1
                        except Error as e:
                            messagebox.showerror("SQL Error", f"Error in command: {command}\nError: {e}")
                            break
                
                self.cxn.commit()
                messagebox.showinfo("Success", f"Successfully executed {success_count} commands")
                
            except Exception as e:
                messagebox.showerror("File Error", f"Error reading file: {e}")
    
    def lookup_info(self):
        # Create lookup dialog
        lookup_window = tk.Toplevel(self.root)
        lookup_window.title("Lookup Information")
        lookup_window.geometry("600x500")
        
        # Table selection
        tk.Label(lookup_window, text="Select Table:", font=('Arial', 12)).pack(pady=10)
        
        table_var = tk.StringVar()
        table_combo = ttk.Combobox(lookup_window, textvariable=table_var, 
                                  values=list(self.tables.keys()), font=('Arial', 12))
        table_combo.pack(pady=5)
        
        # Column selection
        tk.Label(lookup_window, text="Select Column (* for all):", font=('Arial', 12)).pack(pady=10)
        column_var = tk.StringVar()
        column_entry = tk.Entry(lookup_window, textvariable=column_var, font=('Arial', 12))
        column_entry.pack(pady=5)
        
        # Conditions
        tk.Label(lookup_window, text="Conditions (optional):", font=('Arial', 12)).pack(pady=10)
        condition_var = tk.StringVar()
        condition_entry = tk.Entry(lookup_window, textvariable=condition_var, font=('Arial', 12))
        condition_entry.pack(pady=5)
        
        def execute_lookup():
            table = table_var.get()
            column = column_var.get() if column_var.get() else "*"
            condition = condition_var.get()
            
            if not table:
                messagebox.showerror("Error", "Please select a table")
                return
            
            try:
                if condition:
                    sql = f"SELECT {column} FROM {table} WHERE {condition}"
                else:
                    sql = f"SELECT {column} FROM {table}"
                
                self.cur.execute(sql)
                lookup_window.destroy()
                self.display_results()
                
            except Error as e:
                messagebox.showerror("SQL Error", f"Error executing query: {e}")
        
        tk.Button(lookup_window, text="Execute", font=('Arial', 12), 
                 bg='#2ecc71', fg='white', command=execute_lookup).pack(pady=20)
    
    def insert_data(self):
        # Create insert dialog
        insert_window = tk.Toplevel(self.root)
        insert_window.title("Insert Data")
        insert_window.geometry("600x500")
        
        # Table selection
        tk.Label(insert_window, text="Select Table:", font=('Arial', 12)).pack(pady=10)
        
        table_var = tk.StringVar()
        table_combo = ttk.Combobox(insert_window, textvariable=table_var, 
                                  values=list(self.tables.keys()), font=('Arial', 12))
        table_combo.pack(pady=5)
        
        # Frame for entry fields
        entry_frame = tk.Frame(insert_window)
        entry_frame.pack(pady=20, fill='both', expand=True)
        
        entries = {}
        
        def create_entry_fields():
            table = table_var.get()
            if not table:
                return
            
            # Clear previous entries
            for widget in entry_frame.winfo_children():
                widget.destroy()
            entries.clear()
            
            # Create entry fields for each column
            for i, column in enumerate(self.tables[table]):
                tk.Label(entry_frame, text=f"{column}:", font=('Arial', 10)).grid(row=i, column=0, padx=10, pady=5, sticky='e')
                entry = tk.Entry(entry_frame, font=('Arial', 10))
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries[column] = entry
        
        table_combo.bind('<<ComboboxSelected>>', lambda e: create_entry_fields())
        
        def execute_insert():
            table = table_var.get()
            if not table:
                messagebox.showerror("Error", "Please select a table")
                return
            
            values = []
            for column in self.tables[table]:
                value = entries[column].get()
                values.append(value)
            
            try:
                placeholders = ', '.join(['%s'] * len(values))
                columns = ', '.join(self.tables[table])
                sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                
                self.cur.execute(sql, values)
                self.cxn.commit()
                messagebox.showinfo("Success", "Data inserted successfully")
                insert_window.destroy()
                
            except Error as e:
                messagebox.showerror("SQL Error", f"Error inserting data: {e}")
        
        tk.Button(insert_window, text="Insert", font=('Arial', 12), 
                 bg='#2ecc71', fg='white', command=execute_insert).pack(pady=20)
    
    def update_data(self):
        # Create update dialog
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Data")
        update_window.geometry("600x400")
        
        # Table selection
        tk.Label(update_window, text="Select Table:", font=('Arial', 12)).pack(pady=10)
        
        table_var = tk.StringVar()
        table_combo = ttk.Combobox(update_window, textvariable=table_var, 
                                  values=list(self.tables.keys()), font=('Arial', 12))
        table_combo.pack(pady=5)
        
        # Column to update
        tk.Label(update_window, text="Column to Update:", font=('Arial', 12)).pack(pady=10)
        column_var = tk.StringVar()
        column_entry = tk.Entry(update_window, textvariable=column_var, font=('Arial', 12))
        column_entry.pack(pady=5)
        
        # New value
        tk.Label(update_window, text="New Value:", font=('Arial', 12)).pack(pady=10)
        value_var = tk.StringVar()
        value_entry = tk.Entry(update_window, textvariable=value_var, font=('Arial', 12))
        value_entry.pack(pady=5)
        
        # Condition
        tk.Label(update_window, text="WHERE Condition:", font=('Arial', 12)).pack(pady=10)
        condition_var = tk.StringVar()
        condition_entry = tk.Entry(update_window, textvariable=condition_var, font=('Arial', 12))
        condition_entry.pack(pady=5)
        
        def execute_update():
            table = table_var.get()
            column = column_var.get()
            value = value_var.get()
            condition = condition_var.get()
            
            if not all([table, column, value, condition]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            try:
                sql = f"UPDATE {table} SET {column} = %s WHERE {condition}"
                self.cur.execute(sql, (value,))
                self.cxn.commit()
                messagebox.showinfo("Success", "Data updated successfully")
                update_window.destroy()
                
            except Error as e:
                messagebox.showerror("SQL Error", f"Error updating data: {e}")
        
        tk.Button(update_window, text="Update", font=('Arial', 12), 
                 bg='#f39c12', fg='white', command=execute_update).pack(pady=20)
    
    def delete_data(self):
        # Create delete dialog
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Data")
        delete_window.geometry("500x300")
        
        # Table selection
        tk.Label(delete_window, text="Select Table:", font=('Arial', 12)).pack(pady=10)
        
        table_var = tk.StringVar()
        table_combo = ttk.Combobox(delete_window, textvariable=table_var, 
                                  values=list(self.tables.keys()), font=('Arial', 12))
        table_combo.pack(pady=5)
        
        # Condition
        tk.Label(delete_window, text="WHERE Condition:", font=('Arial', 12)).pack(pady=10)
        condition_var = tk.StringVar()
        condition_entry = tk.Entry(delete_window, textvariable=condition_var, font=('Arial', 12))
        condition_entry.pack(pady=5)
        
        def execute_delete():
            table = table_var.get()
            condition = condition_var.get()
            
            if not all([table, condition]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            # Confirmation dialog
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete from {table}?"):
                try:
                    sql = f"DELETE FROM {table} WHERE {condition}"
                    self.cur.execute(sql)
                    self.cxn.commit()
                    messagebox.showinfo("Success", "Data deleted successfully")
                    delete_window.destroy()
                    
                except Error as e:
                    messagebox.showerror("SQL Error", f"Error deleting data: {e}")
        
        tk.Button(delete_window, text="Delete", font=('Arial', 12), 
                 bg='#e74c3c', fg='white', command=execute_delete).pack(pady=20)
    
    def view_table_guest(self):
        table = self.table_var.get()
        if not table:
            messagebox.showerror("Error", "Please select a table")
            return
        
        try:
            self.cur.execute(f"SELECT * FROM {table}")
            self.display_results()
        except Error as e:
            messagebox.showerror("SQL Error", f"Error viewing table: {e}")
    
    def display_results(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get results
        results = self.cur.fetchall()
        
        if not results:
            messagebox.showinfo("No Results", "No data found")
            return
        
        # Get column names
        columns = [desc[0] for desc in self.cur.description]
        
        # Configure treeview columns
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # Configure column headings and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')
        
        # Insert data
        for row in results:
            self.tree.insert('', 'end', values=row)
    
    def logout(self):
        if self.cxn:
            self.cxn.close()
        self.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = MuseumDatabaseGUI(root)
    root.mainloop()
