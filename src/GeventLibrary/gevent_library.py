"""
Copyright (c) 2022 Eldad Uzman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# genevt monkey patch should be placed at the top
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
from gevent import monkey

monkey.patch_all(thread=False)
from typing import Any, List

from robotlibcore import DynamicCore  # type: ignore

from .keywords import GeventKeywords


class GeventLibrary(DynamicCore):
    """
    *GeventLibrary* library enables robotframework developers to run a \
    bundle of keywords as coroutines.

    Each keywords gets its own greenlet so that they are executed to completion.


    | *** Settings ***
    | Library             GeventLibrary
    |
    |
    | *** Test Cases ***
    | Test1
    |     Log    Hello World
    |     Create Gevent Bundle    alias=alias1
    |     Add Coroutine           Sleep    1s    alias=alias1
    |     Add Coroutine           Sleep    1s    alias=alias1
    |     ${values}               Run Coroutines    alias=alias1
    |     Log Many                @{values}

    == Calling concurrent keywords ==
    === Multiprocessing ===
    Multiprocessing containing code will not result in error, but waiting for process to end is blocking and the event loop will be hanging
    === Multithreading ===
    Multithreading containing code will not result in error, but waiting for process to end is blocking and the event loop will be hanging
    === gevent ===
    gevent containing code will work properly in a bundle and will be concurrent to the other coroutines.
    === asyncio ===
    asyncio containing code will work properly in a bundle and will be concurrent to the other coroutines.
    """

    libraries: List[Any] = [GeventKeywords()]
    ROBOT_LIBRARY_SCOPE = "Global"
    # ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        # self.ROBOT_LIBRARY_LISTENER = self # currently a listener is not needed...
        DynamicCore.__init__(self, GeventLibrary.libraries)
