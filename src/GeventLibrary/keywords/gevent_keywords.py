"""gevent keywords"""
from contextlib import contextmanager
from collections import OrderedDict
from copy import copy
from typing import List, Optional
from typing import OrderedDict as od
from uuid import uuid4

from gevent import joinall, spawn, pool
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.running.context import EXECUTION_CONTEXTS
from robot.utils import safe_str

from GeventLibrary.exceptions import (
    AliasAlreadyCreated,
    BundleHasNoCoroutines,
    NoBundleCreated,
)


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


@contextmanager
def monkey_patch_robot_ctx():
    """provides a context manager for safe and succinct coroutine execution context"""
    built_in = BuiltIn()

    ctx = EXECUTION_CONTEXTS.current
    ## monkey
    start_keyword_placer = copy(ctx.output.start_keyword)
    end_keyword_placer = copy(ctx.output.end_keyword)

    ctx.output.start_keyword = lambda kw: _start_keyword(kw, built_in)
    ctx.output.end_keyword = lambda kw: _end_keyword(kw, built_in)
    ## end monkey
    try:
        yield built_in
    finally:
        # unmonkey
        ctx.output.start_keyword = start_keyword_placer
        ctx.output.end_keyword = end_keyword_placer
    ## end unmonkey


def _start_keyword(keyword_item, built_in):
    """listener for starting a keyword - drop it as HTML table"""
    html_text = f"""
            <style>
                #demo table, #demo th, #demo td{{
                    border: 1px dotted black;
                    border-collapse: collapse;
                    table-layout: auto;
                }}
            </style>
            <table id="demo" style="width:100%">
                <tr>
                    <th style="width:10%">Event</th>
                    <th style="width:10%">Keyword</th>
                    <th style="width:10%">Args</th>
                    <th style="width:10%">Doc</th>
                </tr>
                <tr>
                    <td style="text-align:center">Started</td>
                    <td style="text-align:center">{keyword_item.name}</td>
                    <td style="text-align:center">{"   ".join([safe_str(a) for a in keyword_item.args])}</td>
                    <td style="text-align:center">{keyword_item.doc}</td>
                </tr>
            </table>

            """
    built_in.log(html_text, html=True)


def _end_keyword(keyword_item, built_in):
    """listener for ending a keyword - drop it as HTML table"""
    html_text = f"""
            <style>
                #demo table, #demo th, #demo td{{
                    border: 1px dotted black;
                    border-collapse: collapse;
                    table-layout: auto;
                }}
                #statusfail{{
                    border: 1px dotted black;
                    color:red;
                    bgcolor:gray;
                    text-align:center;
                    border-collapse: collapse;
                    table-layout: auto;
                    }}
                #statuspass{{
                    border: 1px dotted black;
                    color:green;
                    bgcolor:gray;
                    text-align:center;
                    border-collapse: collapse;
                    table-layout: auto;
                    }}
            </style>
            <table id="demo" style="width:100%">
                <tr>
                    <th style="width:10%">Event</th>
                    <th style="width:10%">Keyword</th>
                    <th style="width:10%">Args</th>
                    <th style="width:10%">Doc</th>
                    <th style="width:10%">Status</th>
                </tr>
                <tr>
                    <td style="text-align:center">Completed</td>
                    <td style="text-align:center">{keyword_item.name}</td>
                    <td style="text-align:center">{"   ".join([safe_str(a) for a in keyword_item.args])}</td>
                    <td style="text-align:center">{keyword_item.doc}</td>
                    <td id="status{keyword_item.result.status.lower()}">{keyword_item.result.status}</td>
                </tr>
            </table>

            """
    built_in.log(html_text, html=True)


class GeventKeywords:
    """class defining gevent keywords"""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

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
    def add_coroutine(
        self,
        keyword_name: str,
        *args,
        alias: str = None,
        **kwargs,
    ):
        """Adding a new keyword to be a coroutine of the bundle,
        If no bundle alias is given, the last created bundle will be used by default
        Examples:

        |       Add Coroutine    Sleep    1s
        |       Add Coroutine    Sleep    1s    alias=alias1
        |       Add Coroutine    Convert To Lower Case    UPPER
        Args:

            ``keyword_name``            <str> Explicit robotframework keyword name

            ``*args``                   <args> all positional arguments of the keywords.

            ``alias``                   <str, optional> Name of alias. Defaults to None.

            ``**kwargs``                <kwargs> all keyword arguments of the keywords
        """
        self[alias].append(RobotKeywordCoroutine(keyword_name, *args, **kwargs))

    @keyword
    def run_coroutines(
        self, alias: str = None, timeout: int = 200, gevent_pool_size: int = 0
    ) -> List:
        """Runs all the coroutines asynchronously.

        Args:

            ``alias``               <str, optional> Name of alias. Defaults to None.

            ``timeout``             <int, optional> Coroutines execution timeout in seconds. Defaults to 200.

            ``gevent_pool_size``    <int> Size of gevent pool, 0 for using spawn without pooling. Defaults to 0.


            |    ${values}    Run Coroutines    alias=alias1

        Returns:

            ``list`` <List[Any]>   all returned values from coroutines by order
        """
        if gevent_pool_size < 0:
            raise ValueError(
                f"'gevent_pool_size' must be a non negative value, got {gevent_pool_size}"
            )
        coros = self[alias]
        if len(coros) == 0:
            raise BundleHasNoCoroutines(
                "The given bundle has no coroutines, please use `Add Coroutine` keyword"
            )
        with monkey_patch_robot_ctx() as built_in:
            spawn_callable = spawn
            if gevent_pool_size > 0:
                spawn_callable = pool.Pool(gevent_pool_size).spawn
            jobs = [
                spawn_callable(
                    built_in.run_keyword,
                    coro.keyword_name,
                    *coro.all_args,
                )
                for coro in coros
            ]

            greenlets = joinall(jobs, timeout=timeout)

        # check for exceptions...
        for greenlet in greenlets:
            if greenlet.exception:
                raise greenlet.exception

        coros.clear()

        return [job.value for job in jobs]

    @keyword
    def clear_bundle(self, alias: str = None):
        """
        removes a single coroutines bundle from the list

        Args:
            ``alias``               <str, optional> Name of alias. Defaults to None.
        """
        try:
            alias = alias or list(self._active_gevent_bundles.items())[-1][0]
            self._active_gevent_bundles.pop(alias).clear()
        except KeyError as ex:
            raise LookupError(f"Bundle with alias {alias} was not found") from ex

    @keyword
    def clear_all_bundles(self):
        """
        removes all coroutines bundles from the list
        """
        self._active_gevent_bundles.clear()

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
