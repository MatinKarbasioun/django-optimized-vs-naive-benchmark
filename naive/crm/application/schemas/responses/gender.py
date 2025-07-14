from enum import Enum


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNDEFINED = 'undefined'
    NON_BINARY = 'non_binary'