.. freqsap documentation master file, created by
   sphinx-quickstart on Wed May  5 22:45:36 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to freqsap's documentation!
==========================================================

freqsap queries frequencies of single amino-acid polymorphisms.

Quickstart
==========

Install from PyPI:

.. code-block:: console

  python -m pip install freqsap

Show command-line help:

.. code-block:: console

  freqsap --help

Run a query:

.. code-block:: console

  freqsap \
    --accession P02792 \
    --regions European,East Asian \
    --output-file P02792_frequency.tsv

Version information
===================

Show CLI version:

.. code-block:: console

  freqsap --version

Show Python package version:

.. code-block:: console

  python -c "import freqsap; print(freqsap.__version__)"

.. toctree::
  :maxdepth: 2
  :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
