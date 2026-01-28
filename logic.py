import csv

class Contact:
    def __init__(self, name, phone_number):
        if not phone_number.isdigit():
            raise ValueError("Phone number must be digits!")
        self.name = name
        self.phone_number = phone_number

class PhoneBook:
    def __init__(self, filename="contacts.csv"):
        self.contacts = []
        self.filename = filename
    
    def add_contact(self, name, phone_number):
        new_contact = Contact(name, phone_number)
        self.contacts.append(new_contact)
    
    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            return self.contacts.pop(index)
        return None
    
    def search_contacts(self, query):
        if not query:
            return self.contacts
        
        results = []
        for contact in self.contacts:
            if query.lower() in contact.name.lower():
                results.append(contact)
        return results
    
    def save_to_csv(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone"])
            for contact in self.contacts:
                writer.writerow([contact.name, contact.phone_number])
    
    def load_from_csv(self):
        self.contacts = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 2:
                        self.add_contact(row[0], row[1])
        except FileNotFoundError:
            pass
    
    def get_all_contacts(self):
        return self.contacts.copy()
    
    def sort_by_name(self):
        self.contacts.sort(key=lambda x: x.name.lower())
    
    def get_count(self):
        return len(self.contacts)