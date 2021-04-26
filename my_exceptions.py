class ConvertingCurrencyBotException(Exception):
    pass

class WrongAmountOfArguments(ConvertingCurrencyBotException):
    def __str__(self):
        return "Wrong amount of arguments. Must be three. Example: RUB USD 1000"

class WrongBaseCurrency(ConvertingCurrencyBotException):
    pass

class WrongQuoteCurrency(ConvertingCurrencyBotException):
    pass

class WrongAmount(ConvertingCurrencyBotException):
    pass
