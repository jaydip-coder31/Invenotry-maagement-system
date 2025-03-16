import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import io
import urllib.request
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from Dashboard import IMS
from Billing import billClass
import sys
import os

# Import email credentials
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from email_config import email_, pass_
except ImportError:
    # Fallback if import fails
    email_ = "your_email@gmail.com"
    pass_ = "your_app_password"

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Login System")
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        
        # Create frames
        self.left_frame = tk.Frame(root, bg="white", width=650)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.right_frame = tk.Frame(root, bg="white", width=700)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Load and display the image
        try:
            image_url = "https://img.freepik.com/free-vector/mobile-login-concept-illustration_114360-83.jpg"
            with urllib.request.urlopen(image_url) as u:
                raw_data = u.read()
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize((600, 600))  # Adjusted image size
            self.img = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.left_frame, image=self.img, bg="white")
            self.image_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.placeholder = tk.Label(self.left_frame, text="Login Image", bg="white", 
                                       font=("Arial", 24), width=20, height=10)
            self.placeholder.pack(pady=50)
        
        # Login form
        self.login_frame = tk.Frame(self.right_frame, bg="white", bd=2, relief=tk.GROOVE, padx=40, pady=40)
        self.login_frame.pack(pady=50, padx=80, ipadx=10, ipady=10)  # Increased padding
        
        # Title
        self.title_font = font.Font(family="Times New Roman", size=32, weight="bold")
        self.title = tk.Label(self.login_frame, text="Login System", font=self.title_font, bg="white")
        self.title.pack(pady=(10, 20))
        
        # Employee ID
        self.id_label = tk.Label(self.login_frame, text="Employee ID", font=("Arial", 16), bg="white")
        self.id_label.pack(anchor="w", pady=(10, 5))
        
        self.id_entry = tk.Entry(self.login_frame, font=("Arial", 16), bd=1, relief=tk.SOLID, width=28)
        self.id_entry.pack(pady=(0, 15), ipady=6)
        
        # Password
        self.password_label = tk.Label(self.login_frame, text="Password", font=("Arial", 16), bg="white")
        self.password_label.pack(anchor="w", pady=(10, 5))
        
        self.password_entry = tk.Entry(self.login_frame, font=("Arial", 16), bd=1, relief=tk.SOLID, width=28, show="*")
        self.password_entry.pack(pady=(0, 20), ipady=6)  # Adjusted spacing
        
        # Login button
        self.login_button = tk.Button(self.login_frame, text="Log In", font=("Arial", 18, "bold"), 
                                     bg="#00a8ff", fg="white", bd=0, width=22, height=1, 
                                     command=self.login)
        self.login_button.pack(pady=15)  # Increased padding
        
        # OR divider
        self.divider_frame = tk.Frame(self.login_frame, bg="white")
        self.divider_frame.pack(fill=tk.X, pady=10)  # Adjusted spacing
        
        self.left_line = tk.Frame(self.divider_frame, bg="#e0e0e0", height=2)
        self.left_line.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.or_label = tk.Label(self.divider_frame, text="OR", font=("Arial", 12, "bold"), bg="white", fg="gray")
        self.or_label.pack(side=tk.LEFT)
        
        self.right_line = tk.Frame(self.divider_frame, bg="#e0e0e0", height=2)
        self.right_line.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Forgot password
        self.forgot_password = tk.Label(self.login_frame, text="Forget Password?", font=("Arial", 14, "bold"), 
                                       bg="white", fg="#0078aa", cursor="hand2")
        self.forgot_password.pack(pady=15)  # Adjusted padding
        self.forgot_password.bind("<Button-1>", self.forgot_password_window)
    
    def login(self):
        employee_id = self.id_entry.get()
        password = self.password_entry.get()
        
        if not employee_id or not password:
            messagebox.showerror("Error", "Please enter both Employee ID and Password")
            return
        
        try:
            # Connect to MySQL database
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Jaydip@1234",
                database="ims"
            )
            cur = con.cursor()
            
            # Check if employee exists with given credentials
            cur.execute("SELECT * FROM employee WHERE eid=%s AND pass=%s", (
                employee_id,
                password
            ))
            row = cur.fetchone()
            
            if row is None:
                messagebox.showerror("Error", "Invalid Employee ID or Password")
            else:
                # Check user type (Admin or Employee)
                user_type = row[8]  # utype column index
                
                # Close login window
                self.root.destroy()
                
                # Open appropriate window based on user type
                if user_type == "Admin":
                    # Open dashboard for admin
                    root = tk.Tk()
                    obj = IMS(root)
                    root.mainloop()
                else:
                    # Open billing page for employee
                    root = tk.Tk()
                    obj = billClass(root)
                    root.mainloop()
            
            con.close()
            
        except mysql.connector.Error as ex:
            messagebox.showerror("Error", f"Database Error: {str(ex)}")
    
    def forgot_password_window(self, event):
        self.forgot_win = tk.Toplevel(self.root)
        self.forgot_win.title("Forgot Password")
        self.forgot_win.geometry("400x350+500+200")
        self.forgot_win.configure(bg="white")
        self.forgot_win.focus_force()
        self.forgot_win.grab_set()
        
        # Title
        title = tk.Label(self.forgot_win, text="Reset Password", font=("Arial", 18, "bold"), bg="white")
        title.pack(pady=20)
        
        # Employee ID
        id_label = tk.Label(self.forgot_win, text="Employee ID", font=("Arial", 14), bg="white")
        id_label.pack(anchor="w", padx=30, pady=(10, 5))
        
        self.reset_id_entry = tk.Entry(self.forgot_win, font=("Arial", 14), bd=1, relief=tk.SOLID)
        self.reset_id_entry.pack(padx=30, pady=(0, 15), ipady=5, fill=tk.X)
        
        # Email
        email_label = tk.Label(self.forgot_win, text="Email", font=("Arial", 14), bg="white")
        email_label.pack(anchor="w", padx=30, pady=(10, 5))
        
        self.reset_email_entry = tk.Entry(self.forgot_win, font=("Arial", 14), bd=1, relief=tk.SOLID)
        self.reset_email_entry.pack(padx=30, pady=(0, 15), ipady=5, fill=tk.X)
        
        # Submit button
        submit_button = tk.Button(self.forgot_win, text="Send OTP", font=("Arial", 14, "bold"), 
                                 bg="#00a8ff", fg="white", bd=0, command=self.send_otp)
        submit_button.pack(pady=20, padx=30, ipady=5, fill=tk.X)
        
        # Store employee data for later use
        self.employee_data = None
        self.otp = None
    
    def send_otp(self):
        employee_id = self.reset_id_entry.get()
        email = self.reset_email_entry.get()
        
        if not employee_id or not email:
            messagebox.showerror("Error", "Please enter both Employee ID and Email", parent=self.forgot_win)
            return
        
        try:
            # Connect to MySQL database
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Jaydip@1234",
                database="ims"
            )
            cur = con.cursor()
            
            # Check if employee exists with given ID and email
            cur.execute("SELECT * FROM employee WHERE eid=%s AND email=%s", (
                employee_id,
                email
            ))
            row = cur.fetchone()
            
            if row is None:
                messagebox.showerror("Error", "Invalid Employee ID or Email", parent=self.forgot_win)
            else:
                # Store employee data
                self.employee_data = row
                
                # Generate OTP
                self.otp = ''.join(random.choice(string.digits) for i in range(6))
                
                # Send email with OTP
                if self.send_otp_email(email, self.otp):
                    # Close current window
                    self.forgot_win.destroy()
                    
                    # Open OTP verification window
                    self.open_otp_verification_window(employee_id, email)
                else:
                    messagebox.showerror("Error", "Failed to send OTP. Please try again.", parent=self.forgot_win)
            
            con.close()
            
        except mysql.connector.Error as ex:
            messagebox.showerror("Error", f"Database Error: {str(ex)}", parent=self.forgot_win)
    
    def send_otp_email(self, email, otp):
        try:
            # Email configuration - using imported credentials
            sender_email = email_  # From imported email_config
            sender_password = pass_  # From imported email_config
            
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "Password Reset OTP - Inventory Management System"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>Password Reset OTP</h2>
                <p>Your OTP for password reset is: <strong>{otp}</strong></p>
                <p>This OTP is valid for 10 minutes.</p>
                <p>Regards,<br>IMS Team</p>
            </body>
            </html>
            """
            
            message.attach(MIMEText(body, "html"))
            
            # Connect to SMTP server
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            print(f"OTP email sent to {email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def open_otp_verification_window(self, employee_id, email):
        self.otp_win = tk.Toplevel(self.root)
        self.otp_win.title("OTP Verification")
        self.otp_win.geometry("400x450+500+200")
        self.otp_win.configure(bg="white")
        self.otp_win.focus_force()
        self.otp_win.grab_set()
        
        # Title
        title = tk.Label(self.otp_win, text="OTP Verification", font=("Arial", 18, "bold"), bg="white")
        title.pack(pady=20)
        
        # OTP Entry
        otp_label = tk.Label(self.otp_win, text="Enter OTP sent to your email", font=("Arial", 14), bg="white")
        otp_label.pack(anchor="w", padx=30, pady=(10, 5))
        
        self.otp_entry = tk.Entry(self.otp_win, font=("Arial", 14), bd=1, relief=tk.SOLID)
        self.otp_entry.pack(padx=30, pady=(0, 15), ipady=5, fill=tk.X)
        
        # New Password
        new_pass_label = tk.Label(self.otp_win, text="New Password", font=("Arial", 14), bg="white")
        new_pass_label.pack(anchor="w", padx=30, pady=(10, 5))
        
        self.new_pass_entry = tk.Entry(self.otp_win, font=("Arial", 14), bd=1, relief=tk.SOLID, show="*")
        self.new_pass_entry.pack(padx=30, pady=(0, 15), ipady=5, fill=tk.X)
        
        # Confirm Password
        confirm_pass_label = tk.Label(self.otp_win, text="Confirm Password", font=("Arial", 14), bg="white")
        confirm_pass_label.pack(anchor="w", padx=30, pady=(10, 5))
        
        self.confirm_pass_entry = tk.Entry(self.otp_win, font=("Arial", 14), bd=1, relief=tk.SOLID, show="*")
        self.confirm_pass_entry.pack(padx=30, pady=(0, 15), ipady=5, fill=tk.X)
        
        # Submit button
        submit_button = tk.Button(self.otp_win, text="Reset Password", font=("Arial", 14, "bold"), 
                                 bg="#00a8ff", fg="white", bd=0, command=lambda: self.verify_otp_and_reset(employee_id))
        submit_button.pack(pady=20, padx=30, ipady=5, fill=tk.X)
        
        # Resend OTP link
        resend_frame = tk.Frame(self.otp_win, bg="white")
        resend_frame.pack(fill=tk.X, padx=30)
        
        resend_label = tk.Label(resend_frame, text="Didn't receive OTP? ", font=("Arial", 12), bg="white")
        resend_label.pack(side=tk.LEFT)
        
        resend_link = tk.Label(resend_frame, text="Resend", font=("Arial", 12, "bold"), 
                              bg="white", fg="#0078aa", cursor="hand2")
        resend_link.pack(side=tk.LEFT)
        resend_link.bind("<Button-1>", lambda event: self.resend_otp(email))
    
    def verify_otp_and_reset(self, employee_id):
        entered_otp = self.otp_entry.get()
        new_password = self.new_pass_entry.get()
        confirm_password = self.confirm_pass_entry.get()
        
        if not entered_otp or not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill all fields", parent=self.otp_win)
            return
        
        if entered_otp != self.otp:
            messagebox.showerror("Error", "Invalid OTP. Please try again.", parent=self.otp_win)
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match", parent=self.otp_win)
            return
        
        if len(new_password) < 6:
            messagebox.showerror("Error", "Password should be at least 6 characters", parent=self.otp_win)
            return
        
        try:
            # Connect to MySQL database
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Jaydip@1234",
                database="ims"
            )
            cur = con.cursor()
            
            # Update password in database
            cur.execute("UPDATE employee SET pass=%s WHERE eid=%s", (
                new_password,
                employee_id
            ))
            con.commit()
            
            messagebox.showinfo("Success", "Password has been reset successfully.", parent=self.otp_win)
            self.otp_win.destroy()
            
            con.close()
            
        except mysql.connector.Error as ex:
            messagebox.showerror("Error", f"Database Error: {str(ex)}", parent=self.otp_win)
    
    def resend_otp(self, email):
        # Generate new OTP
        self.otp = ''.join(random.choice(string.digits) for i in range(6))
        
        # Send email with new OTP
        if self.send_otp_email(email, self.otp):
            messagebox.showinfo("Success", "OTP has been resent to your email.", parent=self.otp_win)
        else:
            messagebox.showerror("Error", "Failed to send OTP. Please try again.", parent=self.otp_win)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSystem(root)
    root.mainloop()
