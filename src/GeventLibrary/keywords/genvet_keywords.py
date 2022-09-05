# from gevent import monkey
# monkey.patch_all()
from collections import OrderedDict
from typing import Callable, List
from typing import OrderedDict as od
from uuid import uuid4

from gevent import joinall, spawn
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn


class RobotKeywordCoroutine:
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


def run_keyword_event(callable: Callable) -> Callable:
    def inner(*args, **kwargs):
        print("doing stuff...")
        return callable(*args, **kwargs)

    return inner


class NoSessionCreated(Exception):
    pass


class SessionHasNoCoroutines(Exception):
    pass


class GeventKeywords:
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
    def create_session(self, alias: str = None):
        alias = alias or str(uuid4())
        self._active_gevent_sessions[alias] = []

    @keyword
    def add_coroutine(self, keyword_name: str, *args, alias: str = None, **kwargs):

        sessions_coros = self._get_session_coroutines(alias=alias)
        sessions_coros.append(RobotKeywordCoroutine(keyword_name, *args, **kwargs))

    @keyword
    def run_coroutines(self, alias: str = None):
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
        return ([job.value for job in jobs],)
