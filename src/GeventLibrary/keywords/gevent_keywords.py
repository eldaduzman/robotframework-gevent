"""gevent keywords"""

from collections import OrderedDict
from typing import List, Optional
from typing import OrderedDict as od
from uuid import uuid4

from gevent import joinall, spawn
from GeventLibrary.exceptions import (
    AliasAlreadyCreated,
    NoBundleCreated,
    BundleHasNoCoroutines,
)
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn


class RobotKeywordCoroutine:
    """Class defining a keywords for coroutine"""

    def __init__(self, keyword_name, *args, **kwargs) -> None:
        self._keyword_name = keyword_name
        self._args = args
        self._kwargs = kwargs

    @property
    def keyword_name(self):
        """keyword to execute"""
        return self._keyword_name

    @property
    def all_args(self):
        """args and kwargs in robotframework format"""
        return [
            *self._args,
            *[f"{key}={value}" for key, value in self._kwargs.items()],
        ]


class GeventKeywords:
    """class defining gevent keywords"""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self) -> None:
        self._active_gevent_bundles: od[
            str, List[RobotKeywordCoroutine]
        ] = OrderedDict()

    @keyword
    def create_gevent_bundle(self, alias: str = None):
        """this methods creates a bundle for coroutines to run,
        once the bundle is created you can attach keywords to it
        these keywords will be executed asynchronously when `Run Coroutines` is called
        Examples:

        |     Create Gevent Bundle
        |     Create Gevent Bundle    alias=alias1

        Args:

            ``alias`` <str, optional> Name of alias. Defaults to None.

        """
        alias = alias or str(uuid4())
        if alias in self._active_gevent_bundles:
            raise AliasAlreadyCreated(
                f"An alias with name {alias} has already been created."
            )
        self._active_gevent_bundles[alias] = []

    @keyword
    def add_coroutine(self, keyword_name: str, *args, alias: str = None, **kwargs):
        """Adding a new keyword to be a coroutine of the bundle,
        If no bundle alias is given, the last created bundle will be used by default
        Examples:

        |       Add Coroutine    Sleep    1s
        |       Add Coroutine    Sleep    1s    alias=alias1
        |       Add Coroutine    Convert To Lower Case    UPPER
        Args:

            ``keyword_name`` <str> Explicit robotframework keyword name

            ``*args``        <args> all positional arguments of the keywords

            ``alias``        <str, optional> Name of alias. Defaults to None.
            
            ``**kwargs``       <kwargs> all keyword arguments of the keywords
        """
        self[alias].append(RobotKeywordCoroutine(keyword_name, *args, **kwargs))

    @keyword
    def run_coroutines(self, alias: str = None, timeout: int = 200) -> List:
        """Runs all the coroutines asynchronously.

        Args:

            ``alias``       <str, optional> Name of alias. Defaults to None.

            ``timeout``     <int, optional> Coroutines execution timeout in seconds. Defaults to 200.


            |    ${values}    Run Coroutines    alias=alias1

        Returns:

            ``list`` <List[Any]>   all returned values from coroutines by order
        """
        coros = self[alias]
        if len(coros) == 0:
            raise BundleHasNoCoroutines(
                "The given bundle has no coroutines, please use `Add Coroutine` keyword"
            )
        built_in = BuiltIn()
        jobs = [
            spawn(
                built_in.run_keyword,
                coro.keyword_name,
                *coro.all_args,
            )
            for coro in coros
        ]

        greenlets = joinall(jobs, timeout=timeout)
        coros.clear()
        # check for exceptions...
        for greenlet in greenlets:
            if greenlet.exception:
                raise greenlet.exception
        return [job.value for job in jobs]

    def __len__(self):
        return len(self._active_gevent_bundles)

    def __getitem__(self, alias: Optional[str] = None) -> List[RobotKeywordCoroutine]:
        if len(self._active_gevent_bundles) == 0:
            raise NoBundleCreated(
                "Please create a bundle with `Create Gevent Bundle` keyword"
            )

        if alias:
            if alias not in self._active_gevent_bundles:
                raise LookupError(f"Bundle with alias {alias} was not found")
            return self._active_gevent_bundles[alias]
        return list(self._active_gevent_bundles.items())[-1][1]
