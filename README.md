# Pytest fixture bug

Run `pytest` in the root of this repository. If the bug still resides within pytest the tests will fail.

* `conftest.py` contains a single session scoped fixture (`recursive_fixture`) that recursively uses a parameterized 
  fixture as a fixture (`parameterized_fixture`).
* `test_foo.py` overrides the `parameterized_fixture` with a fixture that is parameterized. Furthermore it contains  
  a test that uses the `recursive_fixture` as a fixture.
* `test_bar.py` also overrides the `parameterized_fixture` with a fixture that is parameterized. It also contains a test 
  that uses the `recursive_fixture` as a fixture.
  
What can be observed when running `pytest` is that `test_foo` is indirectly passed the fixture result from the 
fixture defined in `test_bar`.

Running `pytest -s` results in:

```
test_bar.py Calling parameterized_fixture with: bar1
Calling recursive_fixture with: bar1
Calling test_foo with: bar1
.
test_foo.py Calling parameterized_fixture with: foo1
Calling test_bar with: bar1
FCalling parameterized_fixture with: foo2
Calling recursive_fixture with: foo2
Calling test_bar with: foo2
.
```

This shows that the `parameterized_fixture` is called but the `recursive_fixture` is not called again, but only for the
first invocation of `test_foo`. Everything works fine for the second parameter.

Running `pytest --setup-show` results in 

```
test_bar.py
SETUP    S parameterized_fixture[bar1]
SETUP    S recursive_fixture (fixtures used: parameterized_fixture)
        test_bar.py::test_bar[bar1] (fixtures used: parameterized_fixture, recursive_fixture).
test_foo.py
SETUP    S parameterized_fixture[foo1]
        test_foo.py::test_foo[foo1] (fixtures used: parameterized_fixture, recursive_fixture)F
TEARDOWN S recursive_fixture
TEARDOWN S parameterized_fixture[foo1]
SETUP    S parameterized_fixture[foo2]
SETUP    S recursive_fixture (fixtures used: parameterized_fixture)
        test_foo.py::test_foo[foo2] (fixtures used: parameterized_fixture, recursive_fixture).
TEARDOWN S recursive_fixture
TEARDOWN S parameterized_fixture[foo2]
TEARDOWN S parameterized_fixture[bar1]
```

Again, one can observe that the SETUP of `recursive_fixture` is not called for the first parameter of 
`parameterized_test` in `test_foo.py`. Also, the TEARDOWN of `parameterized_fixture[bar1]` appears to be called way to 
late. 

