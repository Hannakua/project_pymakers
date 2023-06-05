import pickle
from collections import UserDict
import re


class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"


class Hashtag(Field):
    def __init__(self, hashtag: str):
        super().__init__(hashtag)

    @Field.value.setter
    def value(self, hashtag):
        if hashtag[0] != '#':
            hashtag = '#' + hashtag
        if not re.match(r"^\#[\w\d]+$", hashtag):
            raise ValueError('Hashtag value is not right it can be only alphabet letters (a-z), numbers (0-9) and _')
        super(Hashtag, Hashtag).value.__set__(self, hashtag)

    def __repr__(self) -> str:
        return f"Hashtag({self.value})"


class Note(Field):
    def __init__(self, value):
        super().__init__(value)


class RecordNote:
    def __init__(self, hashtag, note=None):
        self.hashtag = hashtag
        self.notes = []
        if note is not None:
            self.add_note(note)

    def add_note(self, note):
        if isinstance(note, str):
            self.notes.append(Note(note))
        elif isinstance(note, Note):
            self.notes.append(note)
        else:
            raise ValueError('New note is not string value or Note() object')

    def edit_note(self, old_note, new_note):
        for note in self.notes:
            if note.value == old_note:
                note.value = new_note
                return note

    def show(self):
        for note in self.notes:
            print(note)

    def get_hashtag(self):
        return self.hashtag.value

    def get_note_by_index(self, index):
        if self.notes and index < len(self.notes):
            return self.notes[index]
        else:
            return None

    def __str__(self):
        result = self.hashtag.value
        if self.notes:
            result += ': ' + ', '.join([note.value for note in self.notes])
        return result

    def __repr__(self):
        return f"Record({self.hashtag!r}, {self.notes!r})"


class Notebook(UserDict):
    def __init__(self, record=None):
        super().__init__()
        self.data = {}
        if record is not None:
            self.add_record(record)

    def add_record(self, record):
        self.data[record.get_hashtag()] = record

    def show(self):
        for hashtag, record in self.data.items():
            print(f"{hashtag}:")
            record.show()

    def get_records(self, hashtag):
        return self.data.get(hashtag)

    def save_notes(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_notes(self, filename):
        try:
            with open(filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def search(self, value: str):
        result_by_note = []
        result_by_tag = []
        for tag, record in self.data.items():
            if value in tag:
                result_by_tag.append(record)
                continue
            for note in record.notes:
                if value in note.value:
                    result_by_note.append(record)
                    break
        return result_by_tag + result_by_note

    def __iter__(self):
        return iter(self.data.values())

    def __next__(self):
        if self._iter_index < len(self.data):
            record = list(self.data.values())[self._iter_index]
            self._iter_index += 1
            return record
        else:
            raise StopIteration

    def __str__(self):
        result = ''
        for tag in self.data:
            result += str(self.data[tag]) + '\n'
        return result
