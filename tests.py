from main import validate
import pytest

def testOne():
    d = "2021-3-18"
    x = validate(d)
    assert x == True

def testTwo():
    d = "2020-3-18"
    x = validate(d)
    assert x == True

def testThree():
    d = "2020-8-18"
    x = validate(d)
    assert x == True

def testFour():
    d = "2020-8-8"
    x = validate(d)
    assert x == True
