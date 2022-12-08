import re

from flask import request


def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False


def validate_password(password: str):
    """Password Validator"""
    reg = r"^.*(?=.{8,10})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()_+={}?:~\[\]]+$"
    return validate(password, reg)


def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)


def required(value: str) -> bool:
    return False if value is None or value == '' else True


def numeric(value: int | float) -> bool:
    return True if isinstance(value, (int, float)) else False


def min(value: str, min: float) -> bool:
    return float(value) >= float(min)


def max(value: str, max: float) -> bool:
    return float(value) <= float(max)


class FormRequest:

    def __init__(self):
        pass

    def rules(self) -> dict:
        pass

    def validated(self) -> dict:
        values = request.json

        res = {}

        rules = self.rules()

        for param_name, param_rules in rules.items():
            value = values.get(param_name, '')

            if self.__validate_value(value, param_rules):
                res[param_name] = value
            else:
                raise Exception("Error: '{0}' incorrecto".format(param_name))

        return res

    def __validate_value(self, value: str, rules: list) -> bool:

        for rule in rules:
            parts = rule.split(':')
            fname = parts[0]
            params = parts[1:]

            if not self.__validate_value_rule(value, fname, params):
                return False

        return True

    def __validate_value_rule(self, value: str, rule: str, params: list) -> bool:

        return globals()[rule](value, *params)
