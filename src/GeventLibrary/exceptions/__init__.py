"""all costumed exception objects"""


class NoBundleCreated(Exception):
    pass


class BundleHasNoCoroutines(Exception):
    pass


class AliasAlreadyCreated(Exception):
    pass
