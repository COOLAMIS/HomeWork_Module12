import pickle
from collections import UserDict
from datetime import datetime, date

class PhoneError(Exception):
    ...
    
class BirthdayError(Exception):
    ...

class Field:
    def __init__(self, value):
        self.value = value
        self.__value = None
    def __str__(self):
        return self.value
    def __repr__(self) -> str:
        return str(self)
        


class Name(Field):
    ...
    
class Phone(Field):
    
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        if not isinstance(int(value), int):
            raise PhoneError("Phone must be int")
        self.__value = value

    
class Birthday:
    def __init__(self, value):
        self.__value = None
        self.value = value
        
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise BirthdayError()
    
    def __str__(self):
        return self.__value.strftime("%d-%m-%Y")
    
class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday = None):
        self.birthday = birthday
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def change_phone(self, old_phone, new_phone):
        for k,v in enumerate(self.phones):
            if old_phone.value == v.value:
                self.phones[k] = new_phone
                return f"Old phone {old_phone} change to {new_phone}"
        return f"{old_phone} absent for contact {self.name}"
    
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"phone {phone} already exists for contact {self.name}"
    
    def days_to_birthday(self):
        if self.birthday:
            self.birthday = date(self.birthday)
            to_day = date.today()
            current_year = datetime.now().year
            self.birthday = self.birthday.replace(year = current_year)
            delta = to_day - self.birthday
            result = 365 - delta.days
            return result
        return -1
           
    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"
    
   
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return 'Add success'
    
    def iterator(self, n = 3):
        result = ""
        count = 0
        for i, k in self.data.items():
            result += str(i) + str(k) + "\n"
            count += 1
            if count >= n:
                yield result
                count = 0
                result = ""
        if result:
            yield result
    
    def __str__(self) -> str:
        return '\n'.join(str(r) for r in self.data.values())  

    

users_contact = AddressBook()
finded_user = []

list_end = ['good bye', 'close', 'exit']

def decorator_input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError:
            return('Give me correct data please')
        except IndexError:
            return('Give me correct data please')
        except KeyError:
            return('Give me correct data please')
    return wrapper

@decorator_input_error
def hello(*args):
    return 'How can I help you?'

@decorator_input_error
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = users_contact.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return users_contact.add_record(rec)
    

@decorator_input_error
def change_number(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = users_contact.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    users_contact[name] = phone
    return f"no contact {name} in address book"

@decorator_input_error
def phone(*args):
    name_user = args[0]
    phone = args[1]  
    for name, phone in users_contact.items():
        if name_user == name:
            return phone
        
@decorator_input_error
def show_all(*args):
    return users_contact

@decorator_input_error
def show_page(*args):
    page_number = args[0]
    for page in users_contact.iterator(int(page_number)):
        return page

@decorator_input_error
def no_command(*args):
    return 'unknown_command'

@decorator_input_error
def write_data(*args):
    with open ("UserList.bin" , "wb") as file:
        pickle.dump(users_contact, file)
        
@decorator_input_error        
def read_data(*args):
    with open ("UserList.bin" , "rb") as file:
        result = pickle.load(file)
    return result

@decorator_input_error
def find_user(*args):
    search = args[0]
    finded_user.clear()
    for k,v in users_contact.items():
        if search in str(k) or search in str(v):
            res = f'Contact {v}'
            finded_user.append(res)
            return finded_user
    return 'No contact User'

dict_command = {'hello': hello,
                'add': add,
                'change': change_number,
                'phone': phone,
                'show': show_all,
                'page': show_page,
                'write': write_data,
                'read': read_data,
                'find': find_user
                }

def parser(text: str) -> tuple[callable, tuple[str]]:
    text1 = text.split()
    if text1[0] in dict_command.keys():
        return dict_command.get(text1[0]), text.replace(text1[0], '').strip().split()
    return no_command, text

def main():
    while True:
        user_input = input('>>>')
        user_input = user_input.lower()
        
        if user_input in list_end:
            print('Good bye!')
            break
        
        command, data = parser(user_input)
        result = command(*data)
        print(result)
        
        
        
        
if __name__ == '__main__':
    main()