*** Settings ***
Documentation  This is the initial phase for all acceptence tests
...            in this setup, the modules directory is inserted to the sys.path so that the library can be imported
...            by robotframeworks tests
Suite Setup  Arrange Imports


*** Keywords ***

Arrange Imports
  [Documentation]  adding modules directory to the sys.path
  Evaluate  sys.path.insert(1, "src")