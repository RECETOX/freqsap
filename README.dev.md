# `freqsap` developer documentation

If you're looking for user documentation, go [here](README.md).

## Development install

Dependencies are managed with [uv](https://docs.astral.sh/uv/). The `uv.lock` lockfile pins every
dependency (runtime and development) for every supported Python version and platform, so installs
are reproducible; commit it together with `pyproject.toml`.

```shell
# install uv, e.g. (https://docs.astral.sh/uv/getting-started/installation/)
curl -LsSf https://astral.sh/uv/install.sh | sh

# from the project root directory
# create .venv and install freqsap (editable) plus the `dev` dependency group
uv sync

# prefix any command with `uv run` to execute it inside that environment
uv run pytest -v
uv run freqsap --help
```

`uv sync` installs the `dev` group from `[dependency-groups]` by default. To get a runtime-only
environment (e.g. for checking the package as a user would install it), leave the dev tools out:

```shell
uv sync --no-dev
```

The `docs` and `publishing` extras from `[project.optional-dependencies]` are opt-in (they are
added on top of the `dev` group):

```shell
uv sync --extra docs        # dev tools plus the documentation build dependencies
uv sync --extra publishing  # dev tools plus build, twine, wheel
```

To install an extra without the development tools, combine it with `--no-dev`:

```shell
uv sync --no-dev --extra docs
```

If you prefer to manage the environment yourself, plain `pip` still works — development
dependencies are a [PEP 735](https://peps.python.org/pep-0735/) dependency group, so they install
with `pip install --group dev`:

```shell
python -m venv env
source env/bin/activate
python -m pip install --upgrade pip

python -m pip install --no-cache-dir --editable .   # runtime dependencies only
python -m pip install --group dev                   # development dependencies
python -m pip install --no-cache-dir --editable '.[docs]'  # docs extra
```

Note that `pip` ignores `uv.lock` and resolves the newest matching versions, so only the `uv`
workflow above is reproducible.

Throughout the rest of this document, commands are shown with the `uv run` prefix; inside an
activated virtual environment, drop the prefix.

## Running the tests

There are two ways to run tests.

The first way runs the tests in the `uv` environment created by `uv sync` (or in an activated
virtual environment with the development tools installed, where the `uv run` prefix is not needed):

```shell
uv run pytest -v
```

The second is to use `tox`, which can be installed separately (e.g. with `uv tool install tox`), i.e. not necessarily inside the virtual environment you use for installing `freqsap`, but then builds the necessary virtual environments itself by simply running:

```shell
uv run tox
```

Each `tox` environment installs the `dev` dependency group, as configured in
`[tool.tox]legacy_tox_ini`.

Testing with `tox` allows for keeping the testing environment separate from your development environment.
The development environment will typically accumulate (old) packages during development that interfere with testing; this problem is avoided by testing with `tox`.

The CI matrix tests against Python 3.10, 3.11, and 3.12 on Ubuntu, macOS, and Windows.

### Test coverage

In addition to just running the tests to see if they pass, they can be used for coverage statistics, i.e. to determine how much of the package's code is actually executed during tests.
Inside the package directory, run:

```shell
uv run coverage run
```

This runs tests (via `python -m pytest`) and stores the result in a `.coverage` file.
To see the results on the command line, run

```shell
uv run coverage report
```

`coverage` can also generate output in HTML and other formats; see `uv run coverage help` for more information.

Alternatively, use `pytest-cov` directly:

```shell
uv run pytest -v --cov=src/freqsap --cov-report=term-missing
```

## Running linters locally

For linting, import sorting, and formatting we use [ruff](https://docs.astral.sh/ruff/). Running the linters requires the
development tools installed (see [Development install](#development-install)).

```shell
# check for lint errors
uv run ruff check .

# auto-fix lint errors
uv run ruff check . --fix

# check formatting
uv run ruff format --check .

# apply formatting
uv run ruff format .
```

The CI runs both `ruff check` and `ruff format --check` and will fail if either reports issues.

## Generating the API docs

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
uv run make coverage doctest html
```

The HTML output will be in `docs/_build/html`.

You can also run each target individually:

```shell
cd docs

# build HTML only
uv run make html

# find undocumented Python objects
uv run make coverage
cat _build/coverage/python.txt

# test code snippets in documentation
uv run make doctest
```

If you do not have `make`, use `sphinx-build` directly:

```shell
uv run sphinx-build -b html docs docs/_build/html
```

## Versioning

Bumping the version across all files is done with [bump-my-version](https://github.com/callowayproject/bump-my-version), e.g.

```shell
uv run bump-my-version bump major  # bumps from e.g. 1.1.0 to 2.0.0
uv run bump-my-version bump minor  # bumps from e.g. 1.1.0 to 1.2.0
uv run bump-my-version bump patch  # bumps from e.g. 1.1.0 to 1.1.1
```

This updates the version string in all three tracked locations:

- `src/freqsap/__init__.py` — package `__version__` attribute (also exposed via `freqsap --version`)
- `pyproject.toml` — project metadata
- `docs/conf.py` — Sphinx documentation

Because `uv.lock` records the project version, refresh the lockfile after bumping and commit both
files together:

```shell
uv lock
uv lock --check  # fails if pyproject.toml and uv.lock disagree
```

`uv sync --frozen` in CI fails when the two are out of sync, which is exactly what this guards
against.

## Making a release

This section describes how to make a release in 2 parts:

1. preparation
1. making a release on GitHub (which automatically publishes to PyPI)

### (1/2) Preparation

1. Update [CHANGELOG.md](CHANGELOG.md) (don't forget to update links at the bottom of the page).
1. Bump the version using `bump-my-version` (see [Versioning](#versioning)).
1. Refresh the lockfile with `uv lock` and commit `uv.lock` alongside `pyproject.toml`.
1. Run the unit tests with `uv run pytest -v` to confirm everything passes.
1. Push all changes to `main` and verify the [build CI](https://github.com/RECETOX/freqsap/actions/workflows/build.yml) is green.

### (2/2) GitHub release → PyPI

Publishing to PyPI is fully automated via the [publish workflow](https://github.com/RECETOX/freqsap/actions/workflows/publish.yml) using trusted publishing (OIDC — no API tokens required).

To trigger it:

1. [Create a new release on GitHub](https://github.com/RECETOX/freqsap/releases/new), using a tag that matches the bumped version (e.g. `v1.2.0`).
1. Once the release is published, the workflow builds the distribution and uploads it to [PyPI](https://pypi.org/project/freqsap/) automatically.

You can also trigger the publish workflow manually from the [Actions tab](https://github.com/RECETOX/freqsap/actions/workflows/publish.yml) using the **Run workflow** button.