CHECK_DIRS=src/com/qboson/kaiwu
VENV_PATH = ./.venv
export PATH := $(VENV_PATH)/Scripts/:$(PATH)

all_tests: test_install pylint docs-test pytest

test_install:
	pip3 install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

pylint:
	pylint $(CHECK_DIRS)

docs-test:
	pytest --doctest-modules -o doctest_optionflags=NORMALIZE_WHITESPACE $(CHECK_DIRS)

pytest:
	coverage run --source=$(CHECK_DIRS) -m pytest tests
	coverage report