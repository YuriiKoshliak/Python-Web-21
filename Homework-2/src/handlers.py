from src.classes import AddressBook, Record, Notes, BodyOfNote, TegNote, ConsoleUserInterface
from src.cleaner import sorting
import pickle
import re
from pathlib import Path

 
NOTEBOOK = AddressBook()
FILE_NAME = 'data.bin'
FILE_NAME_NOTES = 'data2.bin'
NOTES = Notes()

ui = ConsoleUserInterface()
main_folder_path = None
contacts = {}
phone_pattern = r'\d+'
name_pattern = r'[a-zA-Z_]+'
operator_pattern = r'(edit note)|(add note)|(delete note)|(delete phone)|(show all)|(good bye)|[a-zA-Z_]+\s?'
phone_operator_pattern = r'(add)|(change)|(delete phone)'


# Remove spaces at the beginning and at the end of the string and lower case the string
def operator_handler(operator):
    parced_operator = re.search(operator_pattern, operator)
    return parced_operator.group().lower().strip()

# Defines name and telephone number
def operand_maker(operator):
    operands = []
    trimmedContact = re.sub(phone_operator_pattern, '', operator)
    
    phoneName = re.search(name_pattern, trimmedContact)
    phoneNums = re.findall(phone_pattern, trimmedContact)
    
    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    else:
        operands.append(phoneName.group().capitalize())
    
    if not phoneNums:
        raise Exception('No number? Enter the contact in the format: "Name" "Phone Number"')
    else:
        operands.append(phoneNums)

    return operands

# function to trim operator and name for email, adddress, birthday
def operator_trimmer(pattern: str, operator):
    trimmed = re.sub(pattern, '', operator)
    phoneName = re.search(name_pattern, trimmed).group().capitalize()
    userData = re.sub(phoneName, '', trimmed).strip() if re.search(phoneName, trimmed) \
        else re.sub(phoneName.casefold(), '', trimmed).strip()
    
    return [phoneName, userData]

#Simple welcome function
def hello(operator):
    return 'How can I help you?'

# Adds a phone number to the contacts list
def add_contact(operator):
    phoneName = operand_maker(operator)[0]
    phoneNum = operand_maker(operator)[1]

    record = NOTEBOOK.find(phoneName)
    try:
        if record != None:
            record.add_phone(phoneNum[0])

            return f'Phone to contact {phoneName} has been added!'   
        else:
            new_record = Record(phoneName)
            new_record.add_phone(phoneNum[0])

            NOTEBOOK.add_record(new_record)

            return f'Contact {phoneName} has been added!' 
    except ValueError:
        return "Wrong phone number format!\n"+ \
            "Try using format of 0123456789 - 10 digits, no symbols."

# Adds a birthday to the contacts
def add_birthday(operator):
    contactData = operator_trimmer('birthday', operator)

    record = NOTEBOOK.find(contactData[0])
    if record != None:
        try:
            record.add_birthday(contactData[1])

            return f'Contact {contactData[0]} has a birthday now!'
        except ValueError:
            return 'Wrong date format! Enter the date in format year-month-day!'
    else:
        return f'Woopsie no contact with {contactData[0]} name!' 

# Adds the address to the contacts
def add_address(operator):
    contactData = operator_trimmer('address', operator)

    record = NOTEBOOK.find(contactData[0])
    if record != None:
        record.add_address(contactData[1])

        return f'Contact {contactData[0]} has a address {contactData[1]} now!'   
    else:
        return f'Woopsie no contact with {contactData[0]} name!'

# Adds the email to the contacts
def add_email(operator):
    contactData = operator_trimmer('email', operator)

    record = NOTEBOOK.find(contactData[0])
    if record != None:
        record.email = contactData[1]

        return f'Contact {contactData[0]} has a address {contactData[1]} now!'   
    else:
        return f'Woopsie no contact with {contactData[0]} name!'

# Adds note
def add_note(operator):
    trimmed = re.sub('add note', '', operator).strip()

    if len(trimmed) >= 1:
        NOTEBOOK.write_note(trimmed)

        return 'Note added!'
    else:
        return "You should've write something!"

# Adds tag to the note with specified ID
def add_tag(operator):
    trimmed = re.sub('tag', '', operator).strip()
    index = re.search(r'[0-9]+', trimmed).group()
    tag = re.sub(index, '', trimmed).strip()

    try:
        NOTEBOOK.search_of_note(index)
        if len(tag) >=1:
            NOTEBOOK.add_teg_to_note(index, tag)

            return f'Note {index} has teg: {tag}.'
        else:
            return "Woopsie! You should've written something."
    except ValueError:
        return "ID is incorrect or the note doesnt exist!"

# Finds note with specified ID/Tag/Word
def find_note(operator):
    trimmed = re.sub('note', '', operator).strip()
    try:
        note = NOTEBOOK.search_of_note(trimmed)
        if note is None:
            return "Whoopsie-daisy! Seems like there's no such note."+ \
                "Or is it a typo?" 
        else:
            return note
    except ValueError:
        return "ID is incorrect or the note doesnt exist!"

# Edits note with specified ID
def edit_note(operator):
    trimmed = re.sub('edit note', '', operator).strip()
    index = re.search(r'[0-9]+', trimmed).group()
    new_text = re.sub(index, '', trimmed).strip()
    
    try:
        NOTEBOOK.search_of_note(index)
        if len(new_text) >=1:
            NOTEBOOK.change_note(index, new_text)

            return f'Note {index} was updated!'
        else:
            return "Woopsie! You should've written something."
    except ValueError:
        return "ID is incorrect or the note doesnt exist!"

# Deletes note with specified ID
def delete_note(operator):
    trimmed = re.sub('delete note', '', operator).strip()
    
    try:
        NOTEBOOK.delete_the_note(trimmed)
        return f'Note {trimmed} was deleted!'
    except KeyError:
        return f'No note with that key!'

# This function isn't working so far
def sort_notes(operator): 
    # notes = NOTEBOOK.sorting_of_notes()
    ...
    # return notes

# Shows all notes
def show_notes(operator):
    notes = NOTEBOOK.show_all_notes()
    return ui.display_notes(notes)

# Shows birthdays within certain time range
def show_birthdays(operator):
    trimmed = re.sub('birthdays', '', operator).strip()
    result = NOTEBOOK.list_with_birthdays(int(trimmed))
    if len(result) < 1:
        return f"Oh wow! It seenms like there's no birthdays within {trimmed} days!"
    else:
        return result

# Update the contact number
def change(operator):
    phoneName = operand_maker(operator)[0]
    phoneNums = operand_maker(operator)[1]

    contact = NOTEBOOK.find(phoneName)
    try:
        contact.edit_phone(phoneNums[0], phoneNums[1])

        return f'Contact {phoneName} has been updated!'
    except ValueError:
        return "Wrong phone number format or no such number!\n"+ \
            "Try using format of 0123456789 - 10 digits, no symbols."+ \
                "Or make sure that contact is exist."

# Delete the contact number for a certain contact
def delete_phone(operator):
    phoneName = operand_maker(operator)[0]
    phoneNums = operand_maker(operator)[1]

    contact = NOTEBOOK.find(phoneName)
    try:
        contact.remove_phone(phoneNums[0])

        return f'Phone {phoneNums[0]} was deleted fron contact {phoneName}!'
    except ValueError:
        return "No such phone or there's a typo. "+\
            "Check phone format maybe, it sholuld be 10 digits no symbols."

# Delete the contact
def delete(operator):
    phoneName = re.search(name_pattern, operator.replace("delete", ""))

    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    
    capitalized_name = phoneName.group().capitalize()
    finded = NOTEBOOK.find(capitalized_name)
    if finded != None:
        NOTEBOOK.delete(capitalized_name)

        return f'Contact {capitalized_name} was deleted!'
    else:
        return 'Typo or no such contact!'

# Displays the phone number of the requested contact
def contact(operator):
    phoneName = re.search(name_pattern, operator.replace("contact", ""))

    if not phoneName:
        raise Exception('No name? Enter the contact Name')
    
    capitalized_name = phoneName.group().capitalize()
    record = NOTEBOOK.find(capitalized_name)

    return record

# Shows contact list
def show_all(operator):
    book = NOTEBOOK
    return ui.display_contacts(book)

# Launch cleaner
def launch_cleaner(operator):
    global main_folder_path
    main_folder_path = Path(input('Enter the path for sorting and cleaning: '))
    sorting()

# Simple farewell function
def goodbye(operator):
    save_notebook(operator)
    return 'Your data is saved! Good bye!'

# Saving a notebook
def save_notebook(operator):
    try:
        with open (FILE_NAME, "wb") as file:
            pickle.dump(NOTEBOOK.data, file)

        with open (FILE_NAME_NOTES, "wb") as file2:
            pickle.dump(NOTEBOOK.notes.data, file2)
        
        return "Data was saved to file!"
    except IOError as E:
        return E

# Loadind a notebook
def load_notebook(operator):
    try:
        with open (FILE_NAME, "rb") as file:
            NOTEBOOK.data = pickle.load(file)
        with open (FILE_NAME_NOTES, "rb") as file2:
            NOTEBOOK.notes.data = pickle.load(file2)

        return "Data was loaded from file!"
    except IOError as e:
        return e

# Shows commad list
def commands(operator):
    return ui.display_commands()

OPERATIONS = {
    'hello': hello,
    'add': add_contact,
    'change': change,
    'delete phone': delete_phone,
    'delete': delete,
    'contact': contact,
    'show all': show_all,
    'add note': add_note,
    'note': find_note,
    'delete note': delete_note,
    'edit note': edit_note,
    'notes': show_notes,
    'tag': add_tag,
    'goodbye': goodbye,
    'birthday': add_birthday,
    'birthdays': show_birthdays,
    'address': add_address,
    'save': save_notebook,
    'email': add_email,
    'load': load_notebook,
    'clean': launch_cleaner,
    'help': commands
}

def get_handler(operator):
    operator = operator_handler(operator)
    if operator not in OPERATIONS:
        raise AttributeError
    else:
        return OPERATIONS[operator]

if __name__ == '__main__':
    print('Go to the main file!')