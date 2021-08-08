# -*- coding: utf-8 -*-
"""
Tests of the FleurInput class
"""
from pathlib import Path

from pymatgen.util.testing import PymatgenTest
from pymatgen.io.fleur import FleurInput

TEST_FILES_DIR = Path(__file__).absolute().parent / ".." / ".." / ".." / ".." / "test-files"


class FleurInputTest(PymatgenTest):

    TEST_FILES_DIR = TEST_FILES_DIR

    def test_from_file_inpgen(self):
        """
        Test generation of FleurInput from a inpgen file
        """

        f = FleurInput.from_file(TEST_FILES_DIR / "inp_test")

        param = 5.130606429
        lattice = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]

        title = "A Fleur input generator calculation with aiida"
        parameters = {
            "input": {"cartesian": False},
            "atom": {
                "element": "Si",
                "rmt": 2.1,
                "jri": 981,
                "lmax": 12,
                "lnonsph": 6,
            },
            "comp": {"kmax": 5.0, "gmaxxc": 12.5, "gmax": 15.0},
            "kpt": {"div1": 17, "div2": 17, "div3": 17, "tkb": 0.0005},
        }

        self.assertArrayAlmostEqual(lattice, f.structure.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in f.structure])
        self.assertEqual(fraccoords, [site.frac_coords.tolist() for site in f.structure])
        self.assertEqual(parameters, f.lapw_parameters)
        self.assertEqual(title, f.title)

    def test_from_file_xml(self):
        """
        Test generation of FleurInput from a inp.xml file
        """
        f = FleurInput.from_file(TEST_FILES_DIR / "inp.xml")

        param = 5.1306085
        lattice = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.125, 0.125, 0.125], [-0.125, -0.125, -0.125]]

        title = "Si bulk"
        parameters = {
            "comp": {"jspins": 1, "frcor": False, "ctail": True, "kcrel": 0, "gmax": 11.1, "gmaxxc": 9.2, "kmax": 3.5},
            "atom0": {"rmt": 2.17, "dx": 0.016, "jri": 717, "lmax": 8, "lnonsph": 6, "element": "Si", "lo": "2s 2p"},
            "exco": {"xctyp": "pbe"},
        }

        self.assertArrayAlmostEqual(lattice, f.structure.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in f.structure])
        self.assertEqual(fraccoords, [site.frac_coords.tolist() for site in f.structure])
        self.assertEqual(parameters, f.lapw_parameters)
        self.assertEqual(title, f.title)
