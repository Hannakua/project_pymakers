from classes_for_addressbook import Record, AddressBook, Name, Email, Birthday, Phone
from classes_for_notebook import Notebook, RecordNote, Hashtag

phonebook = AddressBook()
notebook = Notebook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "There is no such name"
        except ValueError as error:
            return str(error)
        except IndexError:
            return "Enter user name"
        except TypeError:
            return "Incorrect values"

    return inner


@input_error
def greeting():
    return "How can I help you?"


def unknown_command():
    return "Unknown command"


@input_error
def exit():
    return None

def help():
    return " add name 0*********/example@email.com/dd.mm.yyyy - додати телефон/емейл/дату народження до контакту name\nnote hashtag note - створити нотатку за вказаним хештегом\nchange name new phone index - змінити номер телефону за вказаним інтексом(якщо не вказувати то зміниться перший)\nmodify hashtag index new_note - змінює нотатку за вказанім хешегом та індексом\nsearch criteria - пошук за вказаною критерією серед емейлів, телефонів та імен\nshow all - показати всі контакти\nshow notes - показати всі нотатки\nphone name - показати всі номера телефонів за вказаним ім'ям\nemail name - показати всі емейли за вказаним ім'ям\nbirthday name - показати дату народження з кількість днів що залишилась до нього\npage page_number number_of_contacts_per_page - показати всі контакти розділені по сторінкам, стандартно перша сторінка та 3 контакти\nnotes page_number number_of_hashtags- показати всі нотатки розділені по сторінкам, стандартно перша сторінка та всі нотаки за одним хештегом"

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
    for name in phonebook.data:
        result += phonebook.show_record(name) + '\n'
    return result.rstrip()


@input_error
def find_user_adressbook(name: str, flag = None):
    if not phonebook.data:
        return "The phonebook is empty"
    result = ''
    if flag is None:
        return phonebook.show_record(name)
    else:
        name = name.lower()
        for user in phonebook.data:
            if name == user.lower():
                result += phonebook.show_record(user) + '\n'
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
def search_by_criteria(criteria: str, flag = None):
    if criteria:
        result = []
        result_str = ''
        for user in phonebook.data:
            record_str = phonebook.show_record(user)
            if flag is not None:
                criteria = criteria.lower()
                record_str = record_str.lower()          
            if record_str.find(criteria) >= 0:
                result.append(record_str)
        for el in result:
            result_str += el +'\n'
        if result == []:
                return f'No records found for that criteria'
        return result_str.rstrip()


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
    "find": find_user_adressbook,
}

filename1 = "address_book.txt"
filename2 = "note_book.txt"


def command_parser(user_input):
    command, *args = user_input.strip().split(' ')
    try:
        handler = commands[command.lower()]

    except KeyError:
        if args:
            command_part2, *args = args[0].strip().split(' ', 1)
            command = command + ' ' + command_part2
        handler = commands.get(command.lower(), unknown_command)

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
