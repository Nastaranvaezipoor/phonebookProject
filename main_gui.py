import tkinter as tk
from tkinter import messagebox
import logic

class PhoneBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PhoneBook Professional")
        self.phonebook = logic.PhoneBook()
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.handle_search)
        
        tk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT)
        
        self.listbox = tk.Listbox(self.root, width=50, height=15)
        self.listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        form_frame = tk.LabelFrame(self.root, text="Contact Information")
        form_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.phone_entry = tk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=1, pady=5)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add", command=self.add_contact, width=12).grid(row=0, column=0, padx=2)
        tk.Button(button_frame, text="Edit", command=self.edit_contact, width=12).grid(row=0, column=1, padx=2)
        tk.Button(button_frame, text="Delete", command=self.delete_contact, width=12).grid(row=0, column=2, padx=2)
        
        tk.Button(button_frame, text="Save to File", command=self.save_data, width=12).grid(row=1, column=0, pady=5)
        tk.Button(button_frame, text="Load from File", command=self.load_data, width=12).grid(row=1, column=1, pady=5)
        tk.Button(button_frame, text="Sort A-Z", command=self.sort_data, width=12).grid(row=1, column=2, pady=5)
        
        tk.Button(self.root, text="Exit", command=self.exit_app, width=20).pack(pady=5)
        
        self.status_label = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_initial_data(self):
        try:
            self.phonebook.load_from_csv()
            self.refresh_list()
            self.set_status(f"Loaded {self.phonebook.get_count()} contacts")
        except Exception as e:
            messagebox.showerror("Error", f"Load error: {str(e)}")
    
    def refresh_list(self, contacts=None):
        self.listbox.delete(0, tk.END)
        
        if contacts is None:
            contacts = self.phonebook.get_all_contacts()
        
        for contact in contacts:
            self.listbox.insert(tk.END, contact.name)
    
    def on_select(self, event=None):
        try:
            selection = self.listbox.curselection()
            if selection:
                index = selection[0]
                selected_name = self.listbox.get(index)
                for contact in self.phonebook.contacts:
                    if contact.name == selected_name:
                        self.name_entry.delete(0, tk.END)
                        self.name_entry.insert(0, contact.name)
                        self.phone_entry.delete(0, tk.END)
                        self.phone_entry.insert(0, contact.phone_number)
                        break
        except:
            pass
    
    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not name or not phone:
            messagebox.showwarning("Error", "Please enter name and phone.")
            return
        
        for contact in self.phonebook.contacts:
            if contact.name.lower() == name.lower():
                messagebox.showwarning("Error", f"There is a contact with this name({name})")
                return
        
        try:
            self.phonebook.add_contact(name, phone)
            self.refresh_list()
            self.clear_form()
            self.set_status("Contact added.")
            messagebox.showinfo("Success", "Contact added successfully")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def edit_contact(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Error", "Select a contact to edit.")
            return
        
        index = selection[0]
        old_name = self.listbox.get(index)
        
        for i, contact in enumerate(self.phonebook.contacts):
            if contact.name == old_name:
                name = self.name_entry.get().strip()
                phone = self.phone_entry.get().strip()
                
                if not name or not phone:
                    messagebox.showwarning("Error", "Please enter name and phone.")
                    return
                
                try:
                    self.phonebook.delete_contact(i)
                    self.phonebook.add_contact(name, phone)
                    self.refresh_list()
                    self.set_status("Contact updated.")
                    messagebox.showinfo("Success", "Contact updated successfully")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                break
    
    def delete_contact(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Error", "Select a contact to delete.")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure to delete this contact?"):
            index = selection[0]
            name = self.listbox.get(index)
            
            for i, contact in enumerate(self.phonebook.contacts):
                if contact.name == name:
                    self.phonebook.delete_contact(i)
                    self.refresh_list()
                    self.clear_form()
                    self.set_status(f"Contact '{name}' deleted.")
                    break
    
    def handle_search(self, event=None):
        query = self.search_entry.get().strip()
        results = self.phonebook.search_contacts(query)
        self.refresh_list(results)
        self.set_status(f"Search results: {len(results)} items")
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.refresh_list()
    
    def save_data(self):
        try:
            self.phonebook.save_to_csv()
            self.set_status("Data saved to file.")
            messagebox.showinfo("Success", "Data saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Save error: {str(e)}")
    
    def load_data(self):
        try:
            self.phonebook.load_from_csv()
            self.refresh_list()
            self.set_status(f"Data loaded - {self.phonebook.get_count()} contacts")
            messagebox.showinfo("Success", "Data loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Load error: {str(e)}")
    
    def sort_data(self):
        self.phonebook.sort_by_name()
        self.refresh_list()
        self.set_status("List sorted alphabetically.")
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
    
    def set_status(self, message):
        self.status_label.config(text=message)
    
    def exit_app(self):
        try:
            self.phonebook.save_to_csv()
        except:
            pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = PhoneBookGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()