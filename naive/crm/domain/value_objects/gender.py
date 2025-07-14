from enum import StrEnum


class Gender(StrEnum):
    UNDEFINED = 'undefined'
    MALE = 'M'
    FEMALE = 'F'
    NONE_BINARY = 'O'

    @classmethod
    def get_genders(cls):
        return [(key.value, key.name) for key in cls]


