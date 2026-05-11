CHECK_DIRS=src/kaiwu
VENV_PATH = ./.venv
export PATH := $(VENV_PATH)/Scripts/:$(PATH)

all_tests: test_install pylint docs-test pytest

test_install:
	python -m pip install -i https://mirrors.aliyun.com/pypi/simple -r devel.txt

pylint:
	python -m pylint $(CHECK_DIRS)

docs-test:
	python -m pytest --doctest-modules -o doctest_optionflags=NORMALIZE_WHITESPACE $(CHECK_DIRS)

pytest:
	python -m coverage run --source=$(CHECK_DIRS) -m pytest tests
	python -m coverage report