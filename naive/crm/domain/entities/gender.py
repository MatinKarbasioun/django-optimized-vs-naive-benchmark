from enum import StrEnum


class Gender(StrEnum):
    UNDEFINED = 'undefined'
    MALE = 'male'
    FEMALE = 'female'
    NONE_BINARY = 'non_binary'

    @classmethod
    def get_genders(cls):
        return [(key.value, key.name) for key in cls]

