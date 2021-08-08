# -*- coding: utf-8 -*-
# Copyright (c)
# Distributed under the terms of the MIT License
#
# FleurInput was adapted from the ExcitingInput class in the pymatgen main package
"""
This module provides functionality and classes for creating pymatgen structures
from fleur input files (http://flapw.de).
"""
from typing import Tuple, Union, Any
from pathlib import Path
from monty.io import zopen
from monty.json import MSONable

from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
from pymatgen.util.typing import PathLike

__all__ = ("FleurInput",)


class FleurInput(MSONable):
    """
    Object for representing the data stored in the structure part of the
    fleur input.

    .. attribute:: structure

        Associated Structure.

    .. attribute:: title

        Optional title string.

    .. attribute:: pbc

        Tuple detemining in which directions there are periodic boundary conditions.

    .. attribute:: lapw_parameters

        Dict with additional LAPW calculation parameters

    """

    def __init__(
        self,
        structure: Structure,
        title: str = None,
        pbc: Tuple[bool, bool, bool] = (True, True, True),
        lapw_parameters: dict = None,
    ):
        """
        Args:
            structure (Structure):  Structure object.
            title (str): Optional title for fleur input. Defaults to unit
                         cell formula of structure. Defaults to None.
            pbc (tuple of bools): Defines in which directions periodic boundary
                                  conditions apply
            lapw_parameters (dict): Defines additional calculation parameters for FLEUR

        """

        if structure.is_ordered:
            self.structure = structure
            self.title = structure.formula if not title else title
            self.pbc = pbc
            if lapw_parameters is None:
                self.lapw_parameters = {}
            else:
                self.lapw_parameters = lapw_parameters
        else:
            raise ValueError("Structure with partial occupancies cannot be " "converted into fleur input!")

    @staticmethod
    def from_string(data: Union[str, bytes], inpgen_input: bool = True, **kwargs) -> "FleurInput":
        """
        Reads the fleur input from a string

        Args:
            data (str or bytes): data to read in
            inpgen_input (bool): if True the input will be presumed to be a inpgen file
                                 otherwise it is parsed into an xml tree and interpreted as a inp.xml file

        Kwargs are passed on to :py:func:`~masci_tools.io.io_fleurxml.load_inpxml()` if the input
        is interpreted as a XML file

        returns: :py:class:`FleurInput` generated from the information read in from the data
        """
        from masci_tools.io.fleur_inpgen import read_inpgen_file
        from masci_tools.io.io_fleurxml import load_inpxml
        from masci_tools.util.xml.xml_getters import get_structure_data, get_parameter_data

        if inpgen_input:
            cell, atoms, pbc, parameters = read_inpgen_file(data, convert_to_angstroem=False)
            title_in = parameters.pop("title", "")
        else:
            xmltree, schema_dict = load_inpxml(data, **kwargs)
            atoms, cell, pbc = get_structure_data(
                xmltree, schema_dict, site_namedtuple=True, convert_to_angstroem=False
            )
            parameters = get_parameter_data(xmltree, schema_dict)
            title_in = parameters.pop("title", "")

        positions, elements, _ = zip(*atoms)
        # create lattice and structure object
        lattice_in = Lattice(cell)
        structure_in = Structure(lattice_in, elements, positions, coords_are_cartesian=True)

        return FleurInput(structure_in, title_in, pbc=pbc, lapw_parameters=parameters)

    @staticmethod
    def from_file(filename: PathLike) -> "FleurInput":
        """
        Reads the fleur input from a file

        Args:
            filename (PathLike): file to read in. If the extension is .xml the the file
                                 will be interpreted as the inp.xml file otherwise it is
                                 assumed to be inpgen input

        returns: :py:class:`FleurInput` generated from the information read in from the file
        """

        inpgen_input = ".xml" not in Path(filename).suffixes

        mode = "rt" if inpgen_input else "rb"

        with zopen(filename, mode) as f:
            data = f.read()

        return FleurInput.from_string(data, inpgen_input=inpgen_input, base_url=filename)

    def get_inpgen_file_content(
        self, parameters: dict = None, ignore_set_parameters: bool = False, **kwargs: Union[int, bool]
    ):
        """
        Produce the inpgen input file corresponding to the given information

        Args:
            parameters (dict): Additional LAPW parameters to use
            ignore_set_parameters (bool): if True only the passed parameters are used and the
                                          ``lapw_parameters`` stored on the instance are ignored

        Kwargs are passed on to :py:func:`~masci_tools.io.fleur_inpgen.write_inpgen_file()`

        returns: str of the inpgen input file
        """
        from masci_tools.io.fleur_inpgen import write_inpgen_file

        if parameters is None:
            parameters = {}

        if not ignore_set_parameters:
            parameters = {**self.lapw_parameters, **parameters}

        if "title" not in parameters:
            parameters["title"] = self.title

        atom_sites = [(site.coords, site.specie.symbol, site.specie.symbol) for site in self.structure.sites]

        return write_inpgen_file(
            self.structure.lattice.matrix,
            atom_sites,
            return_contents=True,
            input_params=parameters,
            convert_from_angstroem=False,
            **kwargs,
        )

    def as_dict(self) -> dict:
        """
        :return: MSONable dict.
        """
        return {
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
            "structure": self.structure.as_dict(),
            "title": self.title,
            "lapw_parameters": self.lapw_parameters,
            "pbc": self.pbc,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FleurInput":
        """
        :param d: Dict representation.
        :return: FleurInput
        """
        return FleurInput(
            Structure.from_dict(d["structure"]),
            title=d["title"],
            lapw_parameters=d["lapw_parameters"],
            pbc=d["pbc"],
        )

    def __repr__(self) -> str:
        return self.get_inpgen_file_content()

    def __str__(self) -> str:
        """
        String representation of Fleurinput file.
        """
        return self.get_inpgen_file_content()

    def write_file(self, filename: PathLike, **kwargs: Any):
        """
        Writes FleurInput to a file.

        .. note::
            Only the inpgen input is supported. Writing out a full
            inp.xml file is not supported

        Args:
            filename (PathLike): file to write the inpgen input to

        Kwargs are passed on to :py:meth:`FleurInput.get_inpgen_file_content()`
        """

        if filename.endswith(".xml"):
            raise ValueError("Writing out of fleur XML files is not supported")

        with zopen(filename, "wt") as f:
            f.write(self.get_inpgen_file_content(**kwargs))
