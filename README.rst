Pymatgen-io-fleur
=========================

This is a `pymatgen <https://pymatgen.org/>`_ IO addon for the LAPW code `fleur <www.flapw.de/>`_. This addon includes:

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

Using from pymatgen ``Structure`` object (Not yet integrated)

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
