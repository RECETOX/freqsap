# `freqsap` developer documentation

If you're looking for user documentation, go [here](README.md).

## Development install

```shell
# Create a virtual environment, e.g. with
python -m venv env

# activate virtual environment
source env/bin/activate

# make sure to have a recent version of pip and setuptools
python -m pip install --upgrade pip setuptools

# (from the project root directory)
# install freqsap as an editable package
python -m pip install --no-cache-dir --editable .
# install development dependencies
python -m pip install --no-cache-dir --editable .[dev]
# install documentation dependencies only
python -m pip install --no-cache-dir --editable .[docs]
```

Afterwards check that the install directory is present in the `PATH` environment variable.

## Running the tests

There are two ways to run tests.

The first way requires an activated virtual environment with the development tools installed:

```shell
python -m pytest -v
```

The second is to use `tox`, which can be installed separately (e.g. with `pip install tox`), i.e. not necessarily inside the virtual environment you use for installing `freqsap`, but then builds the necessary virtual environments itself by simply running:

```shell
tox
```

Testing with `tox` allows for keeping the testing environment separate from your development environment.
The development environment will typically accumulate (old) packages during development that interfere with testing; this problem is avoided by testing with `tox`.

The CI matrix tests against Python 3.10, 3.11, and 3.12 on Ubuntu, macOS, and Windows.

### Test coverage

In addition to just running the tests to see if they pass, they can be used for coverage statistics, i.e. to determine how much of the package's code is actually executed during tests.
In an activated virtual environment with the development tools installed, inside the package directory, run:

```shell
coverage run
```

This runs tests (via `python -m pytest`) and stores the result in a `.coverage` file.
To see the results on the command line, run

```shell
coverage report
```

`coverage` can also generate output in HTML and other formats; see `coverage help` for more information.

Alternatively, use `pytest-cov` directly:

```shell
python -m pytest -v --cov=src/freqsap --cov-report=term-missing
```## Running linters locally

For linting, import sorting, and formatting we use [ruff](https://docs.astral.sh/ruff/). Running the linters requires an
activated virtual environment with the development tools installed.

```shell
# check for lint errors
ruff check .

# auto-fix lint errors
ruff check . --fix

# check formatting
ruff format --check .

# apply formatting
ruff format .
```

The CI runs both `ruff check` and `ruff format --check` and will fail if either reports issues.## Generating the API docs

Building the documentation requires [pandoc](https://pandoc.org/installing.html) in addition to the Python dependencies. Install it via your system package manager, e.g.:

```shell
# Debian/Ubuntu
sudo apt install pandoc

# macOS
brew install pandoc
```

To run the full documentation build (coverage check, doctest, and HTML output) — matching what CI does:

```shell
cd docs
make coverage doctest html
```

The HTML output will be in `docs/_build/html`.

You can also run each target individually:

```shell
cd docs

# build HTML only
make html

# find undocumented Python objects
make coverage
cat _build/coverage/python.txt

# test code snippets in documentation
make doctest
```

If you do not have `make`, use `sphinx-build` directly:

```shell
sphinx-build -b html docs docs/_build/html
```

## Versioning

Bumping the version across all files is done with [bump-my-version](https://github.com/callowayproject/bump-my-version), e.g.

```shell
bump-my-version bump major  # bumps from e.g. 1.1.0 to 2.0.0
bump-my-version bump minor  # bumps from e.g. 1.1.0 to 1.2.0
bump-my-version bump patch  # bumps from e.g. 1.1.0 to 1.1.1
```

This updates the version string in all three tracked locations:

- `src/freqsap/__init__.py` — package `__version__` attribute (also exposed via `freqsap --version`)
- `pyproject.toml` — project metadata
- `docs/conf.py` — Sphinx documentation

## Making a release

This section describes how to make a release in 2 parts:

1. preparation
1. making a release on GitHub (which automatically publishes to PyPI)

### (1/2) Preparation

1. Update [CHANGELOG.md](CHANGELOG.md) (don't forget to update links at the bottom of the page).
1. Bump the version using `bump-my-version` (see [Versioning](#versioning)).
1. Run the unit tests with `python -m pytest -v` to confirm everything passes.
1. Push all changes to `main` and verify the [build CI](https://github.com/RECETOX/freqsap/actions/workflows/build.yml) is green.

### (2/2) GitHub release → PyPI

Publishing to PyPI is fully automated via the [publish workflow](https://github.com/RECETOX/freqsap/actions/workflows/publish.yml) using trusted publishing (OIDC — no API tokens required).

To trigger it:

1. [Create a new release on GitHub](https://github.com/RECETOX/freqsap/releases/new), using a tag that matches the bumped version (e.g. `v1.2.0`).
1. Once the release is published, the workflow builds the distribution and uploads it to [PyPI](https://pypi.org/project/freqsap/) automatically.

You can also trigger the publish workflow manually from the [Actions tab](https://github.com/RECETOX/freqsap/actions/workflows/publish.yml) using the **Run workflow** button.