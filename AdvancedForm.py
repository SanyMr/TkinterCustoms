import tkinter as tk
from tkinter import ttk, messagebox

class AdvancedForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Data Entry Form")
        self.root.geometry("600x700")

        # Main container
        self.main_frame = ttk.Frame(root, padding="10 10 10 10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Basic Information Section
        self.create_basic_section()

        # Advanced Section
        self.create_advanced_section()

        # Save Button
        self.create_save_button()

    def create_basic_section(self):
        """Create basic information section"""
        basic_frame = ttk.LabelFrame(self.main_frame, text="Basic Information")
        basic_frame.pack(fill=tk.X, pady=10, padx=10)

        # Name
        ttk.Label(basic_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(basic_frame, width=50)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Email
        ttk.Label(basic_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_entry = ttk.Entry(basic_frame, width=50)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    def create_advanced_section(self):
        """Create advanced section with expandable functionality"""
        # Advanced Section Frame
        self.advanced_frame = ttk.Frame(self.main_frame)
        self.advanced_frame.pack(fill=tk.X, pady=10, padx=10)

        # Expandable Button
        self.expand_button = ttk.Button(
            self.advanced_frame, 
            text="▼ Advanced Options", 
            command=self.toggle_advanced_section
        )
        self.expand_button.pack(fill=tk.X)

        # Advanced Content Frame (initially hidden)
        self.advanced_content_frame = ttk.Frame(self.advanced_frame)
        
        # Advanced Fields
        ttk.Label(self.advanced_content_frame, text="Phone Number:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.phone_entry = ttk.Entry(self.advanced_content_frame, width=50)
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.advanced_content_frame, text="Address:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.address_entry = ttk.Entry(self.advanced_content_frame, width=50)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.advanced_content_frame, text="Additional Notes:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.notes_text = tk.Text(self.advanced_content_frame, width=38, height=4)
        self.notes_text.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # State variable to track expansion
        self.is_advanced_expanded = False

    def toggle_advanced_section(self):
        """Toggle visibility of advanced section"""
        if not self.is_advanced_expanded:
            # Expand section
            self.advanced_content_frame.pack(fill=tk.X)
            self.expand_button.configure(text="▲ Hide Advanced Options")
            self.is_advanced_expanded = True
        else:
            # Collapse section
            self.advanced_content_frame.pack_forget()
            self.expand_button.configure(text="▼ Advanced Options")
            self.is_advanced_expanded = False

    def create_save_button(self):
        """Create save button"""
        save_frame = ttk.Frame(self.main_frame)
        save_frame.pack(fill=tk.X, pady=10, padx=10)

        save_btn = ttk.Button(save_frame, text="Save", command=self.save_data)
        save_btn.pack(expand=True)

    def save_data(self):
        """Collect and save data from the form"""
        # Collect basic information
        name = self.name_entry.get()
        email = self.email_entry.get()

        # Collect advanced information (if expanded)
        phone = self.phone_entry.get() if self.is_advanced_expanded else "N/A"
        address = self.address_entry.get() if self.is_advanced_expanded else "N/A"
        notes = self.notes_text.get("1.0", tk.END).strip() if self.is_advanced_expanded else "N/A"

        # Validate basic required fields
        if not name or not email:
            messagebox.showerror("Error", "Name and Email are required!")
            return

        # Construct data dictionary
        data = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Address": address,
            "Notes": notes
        }

        # Here you would typically save to a database or file
        messagebox.showinfo("Success", "Data Saved Successfully!\n" + 
                            "\n".join(f"{k}: {v}" for k, v in data.items()))

def main():
    root = tk.Tk()
    app = AdvancedForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
