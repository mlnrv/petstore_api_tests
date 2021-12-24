**Functional autotests for Petstore API service**

How to run functional tests for api:
1. Download project into your computer.
2. In the terminal, change the folder where the downloaded project is located.
3. Enter the command to run virtual environment:

`. bin/create_and_run_virtualenv.sh`

4. Enter the command to run functional tests:

``. bin/run_api_functional_tests.sh``

or you can straight enter pytest command:

``pytest -v --tb=auto -m functional``
