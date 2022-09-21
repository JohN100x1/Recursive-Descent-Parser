class DSLException(Exception):
    pass


class DSLSyntaxError(DSLException):
    pass


class DSLRuntimeError(DSLException):
    pass


class DSLValidationError(DSLException):
    pass
