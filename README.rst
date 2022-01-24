|MIT license| |Github version| |PyPi version| |PyPi pyversion| |Build status| |Coverage status|

Pymatgen-io-fleur
=========================

This is a `pymatgen <https://pymatgen.org/>`_ IO addon for the LAPW code `fleur <https://www.flapw.de/>`_. This addon includes:

* Reading/writing input files for the the fleur input generator (inpgen)
* Reading of xml files used by the main fleur code

Installation
+++++++++++++

.. code-block::

  pip install pymatgen-io-fleur

Usage
++++++

This addon adds a class ``FleurInput`` to the pymatgen IO namespace, which can read in inpgen and inp.xml files and can write inpgen
input back out.

Initializing a ``FleurInput`` from a file

.. code-block:: python

  from pymatgen.io.fleur import FleurInput

  #From inpgen input (automatically detected by missing xml in extension)
  fleur_inp = FleurInput.from_file('inp_example')

  #From XML input
  fleur_inp = FleurInput.from_file('inp.xml')

  #The object has the following attributes
  print(fleur_inp.structure)        #Associated structure
  print(fleur_inp.title)            #Optional title string
  print(fleur_inp.lapw_parameters)  #dict with additional LAPW parameters

Writing inpgen input back out

.. code-block:: python

  fleur_inp.write_file('inp_new')

  #Adding some additional LAPW parameters
  fleur_inp.write_file('inp_new', parameters={'comp': {'kmax': 4.5}})

Usage from pymatgen ``Structure`` object

.. code-block:: python

  from pymatgen.core import Structure

  #inpgen input (filename starts with inp_)
  s = Structure.from_file('inp_test')

  #XML input (filename is of the form inp*.xml)
  s = Structure.from_file('inp.xml')

  s.to('inp_example',format='fleur-inpgen')


License
++++++++

*pymatgen-io-fleur* is distributed under the terms and conditions of the MIT license.

.. |MIT license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE
.. |GitHub version| image:: https://img.shields.io/github/v/tag/JuDFTTeam/pymatgen-io-fleur?include_prereleases&label=GitHub%20version&logo=GitHub
   :target: https://github.com/JuDFTteam/pymatgen-io-fleur/releases
.. |PyPI version| image:: https://img.shields.io/pypi/v/pymatgen-io-fleur
   :target: https://pypi.org/project/pymatgen-io-fleur/
.. |PyPI pyversion| image:: https://img.shields.io/pypi/pyversions/pymatgen-io-fleur
   :target: https://pypi.org/project/pymatgen-io-fleur/
.. |Build status| image:: https://github.com/JuDFTteam/pymatgen-io-fleur/actions/workflows/testing.yml/badge.svg?branch=develop&event=push
   :target: https://github.com/JuDFTteam/pymatgen-io-fleur/actions
.. |Coverage Status| image:: https://codecov.io/gh/JuDFTteam/pymatgen-io-fleur/branch/develop/graph/badge.svg
   :target: https://codecov.io/gh/JuDFTteam/pymatgen-io-fleur
