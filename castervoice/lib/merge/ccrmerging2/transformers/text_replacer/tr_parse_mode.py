class TRParseMode(object):
    """
    type        | replacement location
    ------------------------------------------------------
    ANY         | specs, extras, or defaults
    SPEC        | specs only
    EXTRA       | extras only
    DEFAULT     | defaults only
    NOT_SPECS   | extras and defaults but not specs
    """
    ANY = "<<<ANY>>>"
    SPEC = "<<<SPEC>>>"
    EXTRA = "<<<EXTRA>>>"
    DEFAULT = "<<<DEFAULT>>>"
    NOT_SPECS = "<<<NOT_SPECS>>>"
