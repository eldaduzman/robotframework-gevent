"""all costumed exception objects"""


class NoBundleCreated(Exception):
    """exception when there are no bundles in the library"""


class BundleHasNoCoroutines(Exception):
    """exception when bundle contains no coroutines"""


class AliasAlreadyCreated(Exception):
    """exception bundle alias already exists"""
