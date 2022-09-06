from collections import OrderedDict
from typing import Callable, List
from typing import OrderedDict as od
from uuid import uuid4

from gevent import joinall, spawn
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
        return self._keyword_name

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs


class NoSessionCreated(Exception):
    pass


class SessionHasNoCoroutines(Exception):
    pass


class GeventKeywords:
    """class defining gevent keywords"""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self) -> None:
        self._active_gevent_sessions: od[
            str, List[RobotKeywordCoroutine]
        ] = OrderedDict()

    def _get_session_coroutines(self, alias: str = None):
        if len(self._active_gevent_sessions) == 0:
            raise NoSessionCreated(
                "Please create a session with `Create Session` keyword"
            )

        if alias:
            if alias not in self._active_gevent_sessions:
                raise LookupError(f"session with alias {alias} was not found")
            sessions_coros = self._active_gevent_sessions[alias]
        else:
            sessions_coros = list(self._active_gevent_sessions.items())[-1][1]
        return sessions_coros

    @keyword
    def create_gevent_bundle(self, alias: str = None):
        """this methods creates a session for coroutines to run, once the session is created you can attach keywords to it
        these keywords will be executed asynchronously when `Run Coroutines` is called
        Examples:

        |     Create Gevent Bundle
        |     Create Gevent Bundle    alias=alias1

        Args:
            alias (str, optional): Name of alias. Defaults to None.
        """
        alias = alias or str(uuid4())
        self._active_gevent_sessions[alias] = []

    @keyword
    def add_coroutine(self, keyword_name: str, *args, alias: str = None, **kwargs):
        """Adding a new keyword to be a coroutine of the session,
        If no session alias is given, the last created session will be used by default
        Examples:

        |       Add Coroutine    Sleep    1s
        |       Add Coroutine    Sleep    1s    alias=alias1
        |       Add Coroutine    Convert To Lower Case    UPPER
        Args:
            keyword_name (str): Explicit robotframework keyword name
            *args (args): all positional arguments of the keywords
            alias (str, optional): Name of alias. Defaults to None.
            **args (kwargs): all keyword arguments of the keywords
        """
        sessions_coros = self._get_session_coroutines(alias=alias)
        sessions_coros.append(RobotKeywordCoroutine(keyword_name, *args, **kwargs))

    @keyword
    def run_coroutines(self, alias: str = None) ->List:
        """Runs all the coroutines asynchronously.

        Args:
            alias (str, optional): Name of alias. Defaults to None.

            |    ${values}    Run Coroutines    alias=alias1

        Returns:
            list: all returned values from coroutines
        """
        sessions_coros = self._get_session_coroutines(alias=alias)
        if len(sessions_coros) == 0:
            raise SessionHasNoCoroutines(
                "The given session has no coroutines, please use `Add Coroutine` keyword"
            )
        bi = BuiltIn()
        jobs = [
            spawn(bi.run_keyword, coro.keyword_name, *coro.args)
            for coro in sessions_coros
        ]

        _ = joinall(jobs, timeout=200)
        sessions_coros.clear()
        return [job.value for job in jobs]
