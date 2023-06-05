from classes_for_addressbook import Record, AddressBook, Name, Email, Birthday, Phone
from classes_for_notebook import Notebook, RecordNote, Hashtag

phonebook = AddressBook()
notebook = Notebook()
cashe = ""

def input_error(func):
    def inner(*args, **kwargs):
        global cashe
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            print(find_matching_lines(cashe))
            return "There is no such name"
        except ValueError as error:
            print(find_matching_lines(cashe))
            return str(error)
        except IndexError:
            print(find_matching_lines(cashe))
            return "Enter user name"
        except TypeError:
            print(find_matching_lines(cashe))
            return "Incorrect values"

    return inner


@input_error
def greeting():
    return "How can I help you?"


def unknown_command():
    return "Enter a new command"

def change_command(user_input):
    while True:
        print(find_matching_lines(user_input))
        choice = input('Unknown command. Do you want to change the command? \n(Yes/No): ')
        
        if choice.lower() == 'yes':
            words = user_input.split(' ')
            new_user_input = input('Repeat the command: ')
            if len(words) == 1:
                user_input = new_user_input + user_input[len(new_user_input)+1:]
            elif len(words) >= 2:
                user_input = ' '.join([new_user_input] + words[1:])
            print(user_input)    
            return user_input
        elif choice.lower() == 'no':
            return None
        else:
            print('Please enter "Yes" or "No".')

@input_error
def exit():
    return None

def help():
    return "add name 0*********/example@email.com/dd.mm.yyyy - add a phone/email/birthday to a contact\n"\
           "note hashtag note - create a note with the specified hashtag\n"\
           "change name new_phone index - change the phone number at the specified index (if not specified, the first one will be changed)\n"\
           "modify hashtag index new_note - modify the note with the specified hashtag and index\n"\
           "search criteria - search for criteria among emails, phones, and names\n"\
           "show all - show all contacts\n"\
           "show notes - show all notes\n"\
           "phone name - show all phone numbers for the specified name\n"\
           "email name - show all emails for the specified name\n"\
           "birthday name - show the birthday date with the number of days remaining\n"\
           "page page_number number_of_contacts_per_page - show all contacts divided into pages, default is the first page with 3 contacts\n"\
           "notes page_number number_of_hashtags - show all notes divided into pages, default is the first page with all notes of one hashtag\n"\
           "exit/good bye/close - shutdown/end program"


def find_matching_lines(user_input):
    matching_lines = []
    help_text = help()

    if user_input.strip():
        words = user_input.split()
        first_word = words[0]
        second_word = words[1] if len(words) > 1 else None

        for line in help_text.split('\n'):
            if first_word.lower() in line.lower() and len(first_word) >= 3:
                line = line.strip()
                if line:
                    matching_lines.append(line)
        
        if not matching_lines and second_word:
            for line in help_text.split('\n'):
                if second_word.lower() in line.lower() and len(second_word) >= 3:
                    line = line.strip()
                    if line:
                        matching_lines.append(line)

        if matching_lines:
            matching_lines.insert(0, "Commands in this context:")

    return '\n'.join(matching_lines) + '\n'

@input_error
def add_user(name, contact_details):
    record = phonebook.get_records(name)
    if record:
        return update_user(record, contact_details)
    else:
        if '@' in contact_details:
            record = Record(Name(name), email=Email(contact_details))
        elif '.' in contact_details:
            record = Record(Name(name), birthday=Birthday(contact_details))
        else:
            phone = Phone(contact_details)
            if phone.is_valid_phone():
                record = Record(Name(name), phone=phone)
                phonebook.add_record(record)
                return "Contact successfully added"
            else:
                return "Invalid phone number format"
        phonebook.add_record(record)
        return "Contact successfully added"


@input_error
def add_note(hashtag, note=None):
    record = notebook.get_records(hashtag)
    if record:
        record.add_note(note)
        return f'Note added to {hashtag} successfully'
    else:
        record = RecordNote(Hashtag(hashtag), note=note)
        notebook.add_record(record)
        return f'New {hashtag} added successfully'


def update_user(record, contact_details):
    if '@' in contact_details:
        record.add_email(Email(contact_details))
    elif '.' in contact_details:
        record.add_birthday(Birthday(contact_details))
    else:
        phone = Phone(contact_details)
        if phone.is_valid_phone():
            record.add_phone(phone)
        else:
            return "Invalid phone number format"
    return "Contact details added successfully"


@input_error
def change_phone(name, new_phone, index=0):
    record = phonebook.get_records(name)
    if record:
        if record.phones and '0' <= str(index) < str(len(record.phones)):
            record.edit_phone(old_phone=record.phones[int(index)].value, new_phone=new_phone)
            return "Phone number updated successfully"
        else:
            return "Invalid phone number index"
    else:
        return "There is no such name"


def change_note(hashtag, index, new_note):
    record = notebook.get_records(hashtag)
    if record:
        if record.notes and '0' <= str(index) < str(len(record.notes)):
            record.edit_note(old_note=record.notes[int(index)].value, new_note=new_note)
            return "Note updated successfully"
        else:
            return "Invalid note number index"
    else:
        return "There is no such hashtag"


@input_error
def show_all():
    if not phonebook.data:
        return "The phonebook is empty"
    result = ''
    for name, record in phonebook.data.items():
        result += f'{name}:'
        if record.phones:
            phones = ', '.join([phone.value for phone in record.phones])
            result += f' phones: {phones}'
        if record.emails:
            emails = ', '.join([email.value for email in record.emails])
            result += f' emails: {emails}'
        if record.birthday:
            result += f' birthday: {record.birthday.value}'
            days_left = record.days_to_birthday()
            result += f' days to birthday: {days_left}'
        result += '\n'
    return result.rstrip()


@input_error
def show_notes(criteria=None):
    if not notebook.data:
        return "The notebook is empty"
    if not criteria:
        return str(notebook)

    records = notebook.search(criteria)
    if not records:
        return "No note records found for " + criteria

    result = ''
    for record in records:
        result += str(record) + '\n'
    return result


@input_error
def get_note(hashtag):
    record = notebook.get_records(hashtag)
    if record:
        notes = [f"{note}\n----------------------\n" for note in record.notes]
        if notes:
            notes_str = "".join(notes)
            return f"{hashtag}:\n{notes_str}"
        else:
            return f"No notes found for {hashtag}"
    else:
        return "There is no such hashtag"


@input_error
def get_birthday(name):
    record = phonebook.get_records(name)
    if record:
        if record.birthday:
            return f"{record.name.value}: {record.birthday.value}, Days to birthday: {record.days_to_birthday()}"
        else:
            return "No birthday found for that name"
    else:
        return "There is no such name"

@input_error
def get_phone_number(name):
    record = phonebook.get_records(name)
    if record:
        if record.phones:
            phones = [f"{record.get_name()}: {phone}" for phone in record.phones]
            result = "\n".join(phones)
            return result
        else:
            return "No phone number found for that name"
    else:
        return "There is no such name"


@input_error
def get_email(name):
    record = phonebook.get_records(name)
    if record:
        if record.emails:
            emails = [f"{record.get_name()}: {email}" for email in record.emails]
            result = "\n".join(emails)
            return result

        else:
            return "No email found for that name"

    else:
        return "There is no such name"


@input_error
def search_by_criteria(criteria):
    if criteria:
        result = []
        for record in phonebook.data.values():
            if criteria in record.get_name():
                result.append(record)
            elif any(criteria in email.value for email in record.emails):
                result.append(record)
            elif any(criteria in phone.value for phone in record.phones):
                result.append(record)

        if result:
            result_strings = []
            for record in result:
                contact_info = f"{record.get_name()}"
                if record.phones:
                    phones = ", ".join([phone.value for phone in record.phones])
                    contact_info += f": {phones}"
                if record.emails:
                    emails = ", ".join([email.value for email in record.emails])
                    contact_info += f", Email: {emails}"
                if record.get_birthday():
                    contact_info += f", Birthday: {str(record.get_birthday().value)}"
                    days_left = record.days_to_birthday()
                    contact_info += f", Days to birthday: {days_left}"
                result_strings.append(contact_info)
            return "\n".join(result_strings)

    return "No records found for that criteria"


@input_error
def iteration_note(page=1, count_hashtag=1):
    if not notebook.data:
        return "The notebook is empty"

    page = int(page)
    count_hashtag = int(count_hashtag)
    start_index = (page - 1) * count_hashtag
    end_index = start_index + count_hashtag

    records = list(notebook)
    total_pages = (len(records) + count_hashtag - 1) // count_hashtag

    if page < 1 or page > total_pages:
        return f"Invalid page number. Please enter a page number between 1 and {total_pages}"

    result = ""
    for record in records[start_index:end_index]:
        result += f"{record.hashtag}:\n"
        if record.notes:
            notes = "\n".join([f"{note.value}\n---------------------" for note in record.notes])
            result += f"\n{notes}\n"

    result += f"Page {page}/{total_pages}"

    return result.rstrip()


@input_error
def iteration(page=1, page_size=3):
    if not phonebook.data:
        return "The phonebook is empty"

    page = int(page)
    page_size = int(page_size)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    records = list(phonebook)
    total_pages = (len(records) + page_size - 1) // page_size

    if page < 1 or page > total_pages:
        return f"Invalid page number. Please enter a page number between 1 and {total_pages}"

    result = ""
    for record in records[start_index:end_index]:
        result += f"{record}\n"

    result += f"Page {page}/{total_pages}"

    return result.rstrip()


commands = {
    'hello': greeting,
    'help': help,
    'add': add_user,
    "note": add_note,
    'change': change_phone,
    'show all': show_all,
    'show notes': show_notes,
    "phone": get_phone_number,
    'exit': exit,
    'good bye': exit,
    'close': exit,
    "email": get_email,
    "birthday": get_birthday,
    'search': search_by_criteria,
    "page": iteration,
    "notes": iteration_note,
    "modify": change_note,
}

filename1 = "address_book.txt"
filename2 = "note_book.txt"


def command_parser(user_input):
    command, *args = user_input.strip().split(' ')
    if not command.strip():
        return unknown_command, args
    try:
        handler = commands[command.lower()]

    except KeyError:
        if args:
            command_part2, *args = args[0].strip().split(' ', 1)
            command = command + ' ' + command_part2
        handler = commands.get(command.lower())
        if handler is None:
            user_input = change_command(user_input)
            if user_input is None:
                return unknown_command, args
            return command_parser(user_input)
    if command == "modify":
        args = [args[0], args[1], ' '.join(args[2:])]
    elif command == "note":
        try:
            args = [args[0]] + [' '.join(args[1:])]
        except IndexError:
            pass
    return handler, args


def main():
    phonebook.load_address_book(filename1)
    notebook.load_notes(filename2)

    while True:
        user_input = input(">>> ")

        global cashe
        cashe = user_input

        handler, args = command_parser(user_input)
        result = handler(*args)

        if not result:
            print('Goodbye!')
            phonebook.save_address_book(filename1)
            notebook.save_notes(filename2)
            break
        print(result)


if __name__ == "__main__":
    main()
