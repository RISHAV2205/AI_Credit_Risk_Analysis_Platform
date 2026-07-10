import sys

from src.exception.exception import CreditRiskException

def divide():

    try:

        result = 10 / 0

        return result

    except Exception as e:

        raise CreditRiskException(e, sys)


divide()