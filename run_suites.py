from test_runner import run_tests

# 1️⃣ Run ALL test cases inside the testSuite
#    (i.e. everything under src/test/aquanow/tests)
run_tests("testSuite", open_report=True)

# 2️⃣ Run ONLY specific test file(s) inside testSuite
#    File names are relative to src/test/aquanow/tests
# run_tests("testSuite", files=["test_rfq_auth.py"], open_report=True)