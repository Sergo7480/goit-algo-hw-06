import re
from collections import UserDict

class Field:
    def __init__ (self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)
        
class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Phone must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
        
    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            try:
                phone_obj.value = Phone(new_phone).value
            except ValueError:
                raise ValueError(ValueError("Invalid phone number format. It must be 10 digits."))
        else:
            raise ValueError("Phone number not found.")
    
    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None
    
    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

if __name__ == "__main__":
    
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
     
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
