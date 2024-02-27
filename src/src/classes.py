from collections import UserDict
from datetime import date, datetime
import re


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.__value)
        
class Email(Field):
    def valid(self, value):
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(email_pattern.match(value))

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 0:
            self.__value = value
        else:
            raise ValueError

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value.isnumeric() and len(value) == 10:
            self.__value = value
        else:
            raise ValueError

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        new_val = datetime.strptime(re.sub(r'-', ' ', value), '%Y %m %d')

        if isinstance(new_val, date):
            self.__value = new_val.date()
        else:
            raise ValueError
            
class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 0:
            self.__value = value
        else:
            raise ValueError
    
class Record:
    def __init__(self, name, birthday=None, address=None, email=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None
        self.phones = []
        self._email = None
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is not None:
            email_field = Email(value)
            if email_field.valid(value):
                self._email = email_field.value
            else:
                raise ValueError("Invalid email address")

    def days_to_birthday(self):
        if self.birthday:
            modified_date = self.birthday.value.replace(year=date.today().year + 1) \
            if self.birthday.value.month == 1 \
            else self.birthday.value.replace(year=date.today().year)
        
            result = modified_date - date.today()

            return result.days
        else:
            return f'No B Day :('
        
    def add_phone(self, phone):
        self.phone = Phone(phone)
        self.phones.append(self.phone)

    def add_birthday(self, date):
        try:
            self.birthday = Birthday(date)  
        except:
            raise ValueError

    def add_address(self, address):
        self.address = Address(address)

    def remove_phone(self, phone):
        if phone in [p.value for p in self.phones]:
            for p in self.phones:
                if p.value == phone:
                    self.phones.remove(p)
                    break
        else:
            raise ValueError

    def edit_phone(self, old_phone, new_phone):
        if str(old_phone) not in [p.value for p in self.phones]:
            raise ValueError
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
        
    def find_phone(self, phone):
        phone = str(phone)
        if phone in [p.value for p in self.phones]:
            return Phone(phone)
        else:
            return None
         
    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(p.value for p in self.phones) if self.phones else None}, "
                f"address: {self.address.value if self.address else None}, "
                f"birthday: {self.birthday.value if self.birthday else None}, "
                f"email: {self.email}")

class TegNote(Field):
    def __init__(self, value=None):
        super().__init__(value)

class BodyOfNote(Field):
    def __init__(self, value):
        super().__init__(value)

class Notes(UserDict):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.teg = ''
        self.text = ''

    # def __str__(self):
    #     ...
    
    def add_note(self, body_of_note, teg=None):
        self.count += 1
        self.teg = TegNote(teg)
        self.text = BodyOfNote(body_of_note)
        self.data[self.count] = [self.teg, self.text]
        return self.data[self.count]

    def find_note(self, idx: str):
        if idx.isdigit():
            try:
                return f"ID: {idx}, Tag: {self.data[int(idx)][0].value}, Text: {self.data[int(idx)][1].value}"
            except:
                raise ValueError
        else:
            for key in self.data:
                if self.data[key][0].value != None and \
                 self.data[key][0].value.find(idx) != -1 or self.data[key][1].value.find(idx) != -1:
                    return f"ID: {key}, Tag: {self.teg.value}, Text: {self.text.value}"

                if self.data[key][1].value.find(idx) != -1:
                    return f"ID: {key}, Tag: {self.teg.value}, Text: {self.text.value}"
                else:
                    return f'The search turned up nothing!'
                    
    def delete_note(self, idx):
        if idx.isdigit():
            self.data.pop(int(idx))
        else:
            print('Type the index, please!')

    def edite_note(self, idx, new_text: str):
        self.data[int(idx)][1].value = new_text

    def add_note_teg(self, idx, teg: str):
        try:
            self.data[int(idx)][0].value = teg
        except TypeError:
            return f'Check twice!'

    def sort_note_for_teg(self):
        self.list_tegs = []
        for i in self.data.values():
            self.list_tegs.append(str(i[0]))
        self.list_tegs.sort()
        for n in self.list_tegs:
            for key, value in self.data.items():
                if str(value[0]) == str(n):
                    return self.data.get(key)
                else:
                    continue
                    
class AddressBook(UserDict):
    min_len = 0
    
    def __init__(self):
        super().__init__()
        self.notes = Notes()
        
    def add_record(self, record: Record):
        try:
            self.data[record.name.value] = record   
        except ValueError:
            print('Failed to add the record!')
            
    def find(self, name):
        return self.data[name] if name in self.data else None 
      
    def delete(self, name):
        self.data.pop(name) if name in self.data else None
        
    def write_note(self, body_of_note, teg=None):
        return self.notes.add_note(body_of_note, teg)

    def add_teg_to_note(self, idx, teg):
        return self.notes.add_note_teg(idx,teg)

    def change_note(self, idx, text):
        return self.notes.edite_note(idx, text)

    def search_of_note(self, word):
        return self.notes.find_note(word)

    def sorting_of_notes(self):
        return self.notes.sort_note_for_teg()

    def delete_the_note(self, id):
        return self.notes.delete_note(id)
      
    def show_all_notes(self):
        list = ''
        for i in self.notes.data:
            list += f"ID: {i}, Tag: {self.notes.data[i][0].value}, Text: {self.notes.data[i][1].value} \n"

        return list[:-1]

    def list_with_birthdays(self, days: int):
        list = ''
        for i in filter(lambda i: i.days_to_birthday() < days, self.data.values()):
            list += f'{i}\n'
        
        return list[:-1]
                     
    def __iter__(self):
        return self

    # Shows entire list
    def __next__(self):
        if self.min_len == len(self.data.values()):
            raise StopIteration
        else:
            value = list(self.data.values())[self.min_len]
            self.min_len += 1

            return value

    # Shows certain amount of pages
    def custom_iterator(self, end):
        while end+self.min_len <= len(self.data.values()):
            string_view = ''
            result = list(self.data.values())[self.min_len:end+self.min_len]
            for i in result:
                string_view += f'{i}\n'
            
            yield string_view[:-1]
            
            self.min_len += end+self.min_len

        raise StopIteration    

if __name__ == '__main__':
    book = AddressBook()

    # Creating a record for John
    test_record = Record("John")
    test_record.add_phone("1234567890")
    test_record.add_phone("5555555555")
    test_record.add_birthday("1994-02-20")
    test_record.email = 'test@gmail.com'
    print(test_record)

    test_record1 = Record("Jane")
    test_record1.add_phone("1234567890")
    test_record1.add_phone("5555555555")
    test_record1.add_birthday("1994-02-22")

    test_record2 = Record("Joe")
    test_record2.add_phone("1234567890")
    test_record2.add_phone("5555555555")
    test_record2.add_birthday("1994-02-25")

    # Adding John's record to address book
    book.add_record(test_record)
    book.add_record(test_record1)
    book.add_record(test_record2)
    test_record.add_address('Nowhere')
    print(test_record.address.value)

    print(book.list_with_birthdays(2))

    book.write_note('kjlkjlkklj')
    book.write_note('qweqweqweqwe')
    book.add_teg_to_note(1, 'adad')