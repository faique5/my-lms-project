# my-lms-project
A fully functional web based library management system designed to managed  all the core operations of library.
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector as m
from datetime import datetime, date, timedelta 

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "faique05", 
    "database": "lms"
}
ADMIN_PASSWORD = "123" 

root = None
content_frame = None
current_view = None 

def get_db_connection():
    """Attempts to connect to the database, showing an error if it fails."""
    try:
        return m.connect(**DB_CONFIG)
    except m.Error as err:
        messagebox.showerror("Database Error", f"Failed to connect to MySQL: {err}")
        return None

def clear_content():
    """Clears the dynamic content area."""
    global current_view
    if current_view:
        current_view.destroy()
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)



def db_addbook(bn_entry, ba_entry, c_entry, t_entry, s_entry):
    """Handles the form submission and database insert for adding a book."""
    mydb = get_db_connection()
    if not mydb: return

    bn, ba, c, t_str, s = bn_entry.get(), ba_entry.get(), c_entry.get(), t_entry.get(), s_entry.get()
    
    if not (bn and ba and c and t_str and s):
        messagebox.showwarning("Input Missing", "All fields are required.")
        return

    try:
        t = int(t_str)
        if t <= 0: raise ValueError("Total must be positive.")
        
        data = (bn, ba, c, t, s)
        sql = "INSERT INTO books (bookname, authorname, bcode, totalbook, subject) VALUES (%s, %s, %s, %s, %s);"
        mycur = mydb.cursor()
        mycur.execute(sql, data)
        mydb.commit()

        messagebox.showinfo("Success", f"Book '{bn}' added successfully!")
        draw_admin_menu() 
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Invalid input for Total Books: {ve}")
    except m.Error as err:
        messagebox.showerror("Database Error", f"Failed to add book: {err}")
    finally:
        if mydb and mydb.is_connected(): mydb.close()

def db_deletebook_submit(co_entry):
    """Handles the database deletion of a book based on book code."""
    mydb = get_db_connection()
    if not mydb: return

    co = co_entry.get()
    
    if not co:
        messagebox.showwarning("Input Missing", "Please enter the Book Code.")
        return
    
    if not messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Book Code: {co}? This action is irreversible."):
        if mydb and mydb.is_connected(): mydb.close()
        return

    mycur = mydb.cursor()
    
    try:
        
        delete_sql = "DELETE FROM books WHERE bcode=%s;"
        mycur.execute(delete_sql, (co,))
        mydb.commit()

        if mycur.rowcount > 0:
            messagebox.showinfo("Success", f"Book Code '{co}' successfully deleted from the system.")
        else:
            messagebox.showwarning("Not Found", f"Book Code '{co}' not found in the inventory.")

        draw_admin_menu() 

    except m.Error as err:
        messagebox.showerror("Database Error", f"Deletion failed: {err}")
    finally:
        if mydb and mydb.is_connected(): mydb.close()

def db_dispbook():
    """Displays all books (outputting to a new Toplevel window)."""
    mydb = get_db_connection()
    if not mydb: return
    
    try:
        a = "SELECT bcode, bookname, authorname, totalbook, subject FROM books;" 
        mycur = mydb.cursor()
        mycur.execute(a)
        myresult = mycur.fetchall()
        
        if not myresult:
            messagebox.showinfo("Book Display", "No books found.")
            return

        display_text = "\n".join([
            f"CODE: {i[0]} | NAME: {i[1]} | AUTHOR: {i[2]} | TOTAL: {i[3]}" 
            for i in myresult
        ])
        
        result_window = tk.Toplevel(root)
        result_window.title("Book Inventory")
        text_widget = tk.Text(result_window, wrap=tk.WORD, width=80, height=20)
        text_widget.insert(tk.END, "--- CURRENT BOOK INVENTORY ---\n\n")
        text_widget.insert(tk.END, display_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill='both')

    except m.Error as err:
        messagebox.showerror("Database Error", f"Failed to retrieve data: {err}")
    finally:
        if mydb and mydb.is_connected(): mydb.close()


def db_issuebook_submit(n_entry, r_entry, co_entry, t_entry, q_entry):
    """Handles submission of the issue book form, including validation and stock check."""
    mydb = get_db_connection()
    if not mydb: return

    n, r, co, t_str, q_str = n_entry.get(), r_entry.get(), co_entry.get(), t_entry.get(), q_entry.get()
    
    if not (n and r and co and t_str and q_str):
        messagebox.showwarning("Input Missing", "All fields are required.")
        return

    mycur = mydb.cursor(buffered=True)
    
    try:
        
        q = int(q_str) 
        if q <= 0: raise ValueError("Quantity must be a positive number.")
        
        issue_date_final = None
        try:
            issue_date_final = datetime.strptime(t_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            try:
                issue_date_final = datetime.strptime(t_str, '%Y%m%d').strftime('%Y-%m-%d')
            except ValueError:
                raise ValueError("Date is not in a valid YYYY-MM-DD format.")
        
        stock_sql = "SELECT totalbook FROM books WHERE bcode=%s;"
        mycur.execute(stock_sql, (co,))
        book_record = mycur.fetchone()
        
        if not book_record:
            messagebox.showerror("Error", f"Book Code '{co}' not found in inventory.")
            return

        available_stock = book_record[0]
        if q > available_stock:
            messagebox.showerror("Error", f"Insufficient stock. Available: {available_stock}")
            return
            
        
        issue_data = (n, r, co, issue_date_final, q) 
        insert_issue_sql = "INSERT INTO issue (name, regno, bcode, issuedate, quantityissue) VALUES (%s, %s, %s, %s, %s);"
        mycur.execute(insert_issue_sql, issue_data)

        
        update_stock_sql = "UPDATE books SET totalbook=totalbook-%s WHERE bcode=%s;"
        mycur.execute(update_stock_sql, (q, co))
        
        mydb.commit()
        
        messagebox.showinfo("Success", f"Book(s) issued successfully to {n} (Reg No: {r}).")
        draw_student_menu() 
        
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Validation Failed: {ve}")
    except m.Error as err:
        messagebox.showerror("Database Error", f"Transaction failed: {err}")
    finally:
        if mydb and mydb.is_connected(): mydb.close()


def db_returnbook_submit(n_entry, r_entry, co_entry, rt_entry, q_entry):
    """Handles submission of the return book form (NO fine calculation)."""
    mydb = get_db_connection()
    if not mydb: return

    n, r, co, rt_str, q_str = n_entry.get(), r_entry.get(), co_entry.get(), rt_entry.get(), q_entry.get()
    
    if not (n and r and co and rt_str and q_str):
        messagebox.showwarning("Input Missing", "All fields are required.")
        return

    mycur = mydb.cursor(buffered=True)
    
    try:
        
        q = int(q_str)
        if q <= 0: raise ValueError("Quantity must be a positive number.")
        
        
        return_date = None
        try:
            return_date = datetime.strptime(rt_str, '%Y-%m-%d').date()
        except ValueError:
            try:
                return_date = datetime.strptime(rt_str, '%Y%m%d').date()
            except ValueError:
                raise ValueError("Return Date is not in a valid YYYY-MM-DD format.")
        
        
        check_issue_sql = "SELECT quantityissue FROM issue WHERE regno=%s AND bcode=%s;"
        mycur.execute(check_issue_sql, (r, co))
        issue_record = mycur.fetchone()
        
        if not issue_record:
            messagebox.showerror("Error", f"No matching issue record found for Reg No. {r} and Book {co}.")
            return
            
        issued_quantity = issue_record[0]
        
        if q > issued_quantity:
            messagebox.showerror("Error", f"Cannot return {q} books. Only {issued_quantity} were issued to this registration.")
            return

        
        return_data = (n, r, co, return_date, q) 
        insert_return_sql = "INSERT INTO returnbook (name, regno, bcode, returndate, quantityissue) VALUES (%s, %s, %s, %s, %s);"
        mycur.execute(insert_return_sql, return_data)

        
        delete_issue_sql = "DELETE FROM issue WHERE regno=%s AND bcode=%s AND quantityissue=%s LIMIT 1;"
        mycur.execute(delete_issue_sql, (r, co, issued_quantity))

        
        update_stock_sql = "UPDATE books SET totalbook=totalbook+%s WHERE bcode=%s;"
        mycur.execute(update_stock_sql, (q, co))
        
        mydb.commit()
        
        messagebox.showinfo("Success", f"Book(s) returned successfully.")
        draw_student_menu() 
        
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Validation Failed: {ve}")
    except m.Error as err:
        messagebox.showerror("Database Error", f"Transaction failed: {err}")
    finally:
        if mydb and mydb.is_connected(): mydb.close()

def db_report_issue():
    """Displays all records from the issue table in a Toplevel window."""
    mydb = get_db_connection()
    if not mydb: return
    
    try:
        a = "SELECT regno, bcode, issuedate, quantityissue FROM issue;" 
        mycur = mydb.cursor()
        mycur.execute(a)
        myresult = mycur.fetchall()
        
        if not myresult:
            messagebox.showinfo("Issue Report", "No books are currently issued.")
            return

        display_text = "REG NO. | BOOK CODE | ISSUE DATE | QTY\n"
        display_text += "-" * 50 + "\n"
        display_text += "\n".join([
            f"{i[0]} | {i[1]} | {i[2]} | {i[3]}" 
            for i in myresult
        ])
        
        result_window = tk.Toplevel(root)
        result_window.title("Current Issued Books Report")
        text_widget = tk.Text(result_window, wrap=tk.WORD, width=60, height=20)
        text_widget.insert(tk.END, display_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill='both')

    except m.Error as err:
        messagebox.showerror("Database Error", f"Failed to retrieve issue report: {err}")
    finally:
        if mydb and mydb.is_connected(): mydb.close()


def db_report_return():
    """Displays all records from the returnbook table in a Toplevel window."""
    mydb = get_db_connection()
    if not mydb: return
    
    try:
        a = "SELECT regno, bcode, returndate, quantityissue FROM returnbook;" 
        mycur = mydb.cursor()
        mycur.execute(a)
        myresult = mycur.fetchall()
        
        if not myresult:
            messagebox.showinfo("Return Report", "No book return records found.")
            return

        display_text = "REG NO. | BOOK CODE | RETURN DATE | QTY\n"
        display_text += "-" * 50 + "\n"
        display_text += "\n".join([
            f"{i[0]} | {i[1]} | {i[2]} | {i[3]}" 
            for i in myresult
        ])
        
        result_window = tk.Toplevel(root)
        result_window.title("Book Return History Report")
        text_widget = tk.Text(result_window, wrap=tk.WORD, width=60, height=20)
        text_widget.insert(tk.END, display_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill='both')

    except m.Error as err:
        messagebox.showerror("Database Error", f"Failed to retrieve return report: {err}")
    finally:
        if mydb and mydb.is_connected(): mydb.close()



def draw_reset_password_window():
    """Opens a new window requiring the OLD password before setting the NEW one."""
    
    reset_window = tk.Toplevel(root)
    reset_window.title("Secure Password Reset")
    reset_window.geometry("400x250")
    reset_window.transient(root)
    reset_window.grab_set()

    tk.Label(reset_window, text="Secure Administrator Password Reset", font=("Arial", 12, "bold")).pack(pady=10)

    fields = ["Current Password:", "New Password:", "Confirm New Password:"]
    entries = {}
    
    input_frame = tk.Frame(reset_window)
    input_frame.pack(padx=10)

    for i, label_text in enumerate(fields):
        tk.Label(input_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = tk.Entry(input_frame, show='*', width=30)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[label_text] = entry
    
    def finalize_reset():
        global ADMIN_PASSWORD
        
        old_pass = entries["Current Password:"].get()
        new_pass = entries["New Password:"].get()
        confirm_pass = entries["Confirm New Password:"].get()

        if old_pass != ADMIN_PASSWORD:
            messagebox.showerror("Security Error", "Current Password entered is incorrect.")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Security Error", "New Password and Confirmation do not match.")
            return
            
        if len(new_pass) < 4:
            messagebox.showwarning("Error", "New Password must be at least 4 characters long.")
            return

        ADMIN_PASSWORD = new_pass
        
        messagebox.showinfo("Success", "Password updated successfully! Please log in with your new password.")
        reset_window.destroy()

    tk.Button(reset_window, text="SET NEW PASSWORD", command=finalize_reset, width=25, bg="#FFA500", fg="white").pack(pady=10)
    
    reset_window.bind('<Return>', lambda event=None: finalize_reset())




def draw_start_screen():
    """Draws the initial screen with Student/Admin buttons."""
    global current_view
    clear_content()

    current_view = tk.Frame(content_frame, padx=40, pady=40)
    current_view.pack(expand=True)
    
    tk.Label(current_view, text="MYLIB SYSTEM", font=("Arial", 20, "bold"), fg="#1E90FF").pack(pady=20)

    tk.Button(current_view, text="STUDENT", command=draw_student_menu, width=25, height=2, bg='#90EE90').pack(pady=10)
    tk.Button(current_view, text="ADMINISTRATOR", command=draw_admin_login_window, width=25, height=2, bg='#ADD8E6').pack(pady=10)


def draw_admin_login_window():
    """Draws the password prompt window (Toplevel)."""
    
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x200")
    login_window.transient(root)
    login_window.grab_set()

    tk.Label(login_window, text="Enter Password:", font=("Arial", 10, "bold")).pack(pady=10)

    password_entry = tk.Entry(login_window, show='*', width=25)
    password_entry.pack(pady=5)
    password_entry.focus_set()

    def check_password():
        global ADMIN_PASSWORD 
        if password_entry.get() == ADMIN_PASSWORD:
            login_window.destroy()
            draw_admin_menu() 
        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
            if not messagebox.askretrycancel("Error", "Incorrect password. Try again?"):
                root.quit()
                
    tk.Button(login_window, text="Login", command=check_password, width=10, bg="#4CAF50", fg="white").pack(pady=5)

    tk.Button(login_window, 
              text="Reset Password", 
              command=draw_reset_password_window, 
              width=20, 
              fg='blue').pack(pady=5)

    login_window.bind('<Return>', lambda event=None: check_password())


def draw_student_menu():
    """Draws the Student Tasks Menu."""
    global current_view
    clear_content()

    current_view = tk.LabelFrame(content_frame, text="STUDENT MENU", padx=20, pady=20, font=("Arial", 14, "bold"))
    current_view.pack(padx=10, pady=10, fill="both", expand=True)

    tk.Button(current_view, text=" Display Books", command=db_dispbook, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text=" Issue Book", command=draw_issuebook_form, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text="🔙 Return Book", command=draw_returnbook_form, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text="Exit", command=root.quit, width=30, height=2, bg="#FF6666", fg="white").pack(pady=20)


def draw_admin_menu():
    """Draws the Administrator Tasks Menu."""
    global current_view
    clear_content()

    current_view = tk.LabelFrame(content_frame, text="ADMINISTRATOR MENU", padx=20, pady=20, font=("Arial", 14, "bold"))
    current_view.pack(padx=10, pady=10, fill="both", expand=True)

    tk.Button(current_view, text=" Display Books", command=db_dispbook, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text="➕ Add New Book", command=lambda: draw_addbook_form(), width=30, height=2).pack(pady=5)
    tk.Button(current_view, text="➖ Delete Book", command=draw_deletebook_form, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text=" View Issue Report", command=db_report_issue, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text=" View Return Report", command=db_report_return, width=30, height=2).pack(pady=5) 
    tk.Button(current_view, text=" Main Menu", command=draw_start_screen, width=30, height=2, bg='light gray').pack(pady=10)


def draw_addbook_form():
    """Draws the form to add a new book."""
    global current_view
    clear_content()

    current_view = tk.LabelFrame(content_frame, text="ADD NEW BOOK", padx=20, pady=10, font=("Arial", 14, "bold"))
    current_view.pack(padx=10, pady=10, fill="x")

    fields = ["Book Name:", "Author Name:", "Book Code:", "Total Books (Int):", "Subject:"]
    entries = {}

    for i, label_text in enumerate(fields):
        tk.Label(current_view, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = tk.Entry(current_view, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[label_text.split(':')[0]] = entry

    tk.Button(current_view, text="SUBMIT", 
              command=lambda: db_addbook(
                  entries["Book Name"], entries["Author Name"], entries["Book Code"], 
                  entries["Total Books (Int)"], entries["Subject"]
              ), 
              width=15, bg="#4CAF50").grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    tk.Button(current_view, text="Back to Admin Menu", command=draw_admin_menu, width=15).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)


def draw_deletebook_form():
    """Draws the form for deleting a book."""
    global current_view
    clear_content()

    current_view = tk.LabelFrame(content_frame, text="DELETE BOOK", padx=20, pady=10, font=("Arial", 14, "bold"))
    current_view.pack(padx=10, pady=10, fill="x")

    tk.Label(current_view, text="Book Code:", width=15).grid(row=0, column=0, padx=5, pady=10, sticky='w')
    code_entry = tk.Entry(current_view, width=30)
    code_entry.grid(row=0, column=1, padx=5, pady=10)

    tk.Button(current_view, 
              text="DELETE", 
              command=lambda: db_deletebook_submit(code_entry), 
              width=15, bg="#DC143C", fg="white").grid(row=1, column=0, columnspan=2, pady=10)
    
    tk.Button(current_view, text="Back to Menu", command=draw_admin_menu, width=15).grid(row=2, column=0, columnspan=2, pady=5)


def draw_issuebook_form():
    """Draws the form for issuing a book."""
    global current_view
    clear_content()

    current_view = tk.LabelFrame(content_frame, text="ISSUE BOOK", padx=20, pady=10, font=("Arial", 14, "bold"))
    current_view.pack(padx=10, pady=10, fill="x")

    fields = ["Student Name:", "Reg No.:", "Book Code:", "Issue Date (YYYY-MM-DD):", "Quantity Issue (Int):"]
    entries = {}

    for i, label_text in enumerate(fields):
        tk.Label(current_view, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = tk.Entry(current_view, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[label_text.split(':')[0]] = entry

    tk.Button(current_view, text="ISSUE BOOK", 
              command=lambda: db_issuebook_submit(
                  entries["Student Name"], entries["Reg No."], entries["Book Code"], 
                  entries["Issue Date (YYYY-MM-DD)"], entries["Quantity Issue (Int)"]
              ), 
              width=15, bg="#008CBA", fg="white").grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    tk.Button(current_view, text="Back to Menu", command=draw_student_menu, width=15).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)


def draw_returnbook_form():
    """Draws the form for returning a book."""
    global current_view
    clear_content()

    current_view = tk.LabelFrame(content_frame, text="RETURN BOOK", padx=20, pady=10, font=("Arial", 14, "bold"))
    current_view.pack(padx=10, pady=10, fill="x")

    fields = ["Student Name:", "Reg No.:", "Book Code:", "Return Date (YYYY-MM-DD):", "Quantity Return (Int):"]
    entries = {}

    for i, label_text in enumerate(fields):
        tk.Label(current_view, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = tk.Entry(current_view, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[label_text.split(':')[0]] = entry

    tk.Button(current_view, text="RETURN BOOK", 
              command=lambda: db_returnbook_submit(
                  entries["Student Name"], entries["Reg No."], entries["Book Code"], 
                  entries["Return Date (YYYY-MM-DD)"], entries["Quantity Return (Int)"]
              ), 
              width=15, bg="#FFA07A", fg="white").grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    tk.Button(current_view, text="Back to Menu", command=draw_student_menu, width=15).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

def draw_student_menu():
    """Draws the Student Tasks Menu."""
    global current_view
    clear_content()

    current_view = tk.LabelFrame(content_frame, text="STUDENT MENU", padx=20, pady=20, font=("Arial", 14, "bold"))
    current_view.pack(padx=10, pady=10, fill="both", expand=True)

    tk.Button(current_view, text=" Display Books", command=db_dispbook, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text=" Issue Book", command=draw_issuebook_form, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text="🔙 Return Book", command=draw_returnbook_form, width=30, height=2).pack(pady=5)
    tk.Button(current_view, text="Main Menu",command=draw_start_screen,width=30, height=2, bg="#FF6666", fg="white").pack(pady=20)


def setup_gui():
    """Initializes the Tkinter structure and starts the application."""
    global root, content_frame
    
    root = tk.Tk()
    root.title("MYLIBRO LMS")
    root.geometry("600x550")
    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)
    
    draw_start_screen()
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
