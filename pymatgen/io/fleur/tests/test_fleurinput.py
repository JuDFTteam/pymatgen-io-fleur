# -*- coding: utf-8 -*-
"""
Tests of the FleurInput class
"""
from pathlib import Path
from tempfile import TemporaryDirectory

from pymatgen.util.testing import PymatgenTest
from pymatgen.io.fleur import FleurInput
from pymatgen.core import Structure, Lattice

TEST_FILES_DIR = Path(__file__).absolute().parent / ".." / ".." / ".." / ".." / "test-files"


class FleurInputTest(PymatgenTest):
    """
    Tests of the FleurInput class
    """

    TEST_FILES_DIR = TEST_FILES_DIR

    def test_mson_serializable(self):

        param = 5.130606429
        cell = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]

        title = "Generated pymatgen structure"
        parameters = {
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

        struc = Structure(Lattice(cell), atoms, fraccoords)
        f = FleurInput(struc, title, lapw_parameters=parameters)
        self.assertMSONable(f)

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
        self.assertArrayAlmostEqual(fraccoords, [site.frac_coords.tolist() for site in f.structure])
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
            "atom0": {
                "rmt": 2.17,
                "dx": 0.016,
                "jri": 717,
                "lmax": 8,
                "lnonsph": 6,
                "element": "Si",
                "lo": "2s 2p",
                "id": "14.1",
            },
            "exco": {"xctyp": "pbe"},
        }

        self.assertArrayAlmostEqual(lattice, f.structure.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in f.structure])
        self.assertArrayAlmostEqual(fraccoords, [site.frac_coords.tolist() for site in f.structure])
        self.assertEqual(parameters, f.lapw_parameters)
        self.assertEqual(title, f.title)

    def test_get_inpgen_file_content(self):
        """
        Test of the get_inpgen_file_content method
        """
        param = 5.130606429
        cell = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]

        title = "Generated pymatgen structure"
        parameters = {
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

        struc = Structure(Lattice(cell), atoms, fraccoords)
        f = FleurInput(struc, title, lapw_parameters=parameters)

        expected_inpgen_content = """\
        Generated pymatgen structure
&input  cartesian=F /
       0.000000000        5.130606429        5.130606429
       5.130606429        0.000000000        5.130606429
       5.130606429        5.130606429        0.000000000
      1.0000000000
       1.000000000        1.000000000        1.000000000

      2
         14       0.0000000000       0.0000000000       0.0000000000
         14       0.2500000000       0.2500000000       0.2500000000
&atom
  element="Si"   jri=981   lmax=12   lnonsph=6   rmt=2.1 /
&comp
  gmax=15.0   gmaxxc=12.5   kmax=5.0 /
&kpt
  div1=17   div2=17   div3=17   tkb=0.0005 /
        """

        self.assertTrue(self.assertStrContentEqual(expected_inpgen_content, f.get_inpgen_file_content()))
        self.assertTrue(self.assertStrContentEqual(expected_inpgen_content, str(f)))

    def test_inpgen_file_roundtrip(self):
        """
        Test that the inpgen file can be reproduced reading it in and writing back out
        """
        import tempfile

        f = FleurInput.from_file(TEST_FILES_DIR / "inp_test")

        with open(TEST_FILES_DIR / "inp_test", "r", encoding="utf8") as file:
            original = file.read()

        with tempfile.NamedTemporaryFile(mode="w") as tmp:
            f.write_file(tmp.name)
            with open(tmp.name, "r", encoding="utf8") as inp:
                res = inp.read()

        print(original)
        print(res)
        self.assertTrue(self.assertStrContentEqual(original, res))


class FleurInputStructureIntegrationTest(PymatgenTest):
    """
    Tests of the writing/reading of fleur files from the main pymatgen structure
    """

    TEST_FILES_DIR = TEST_FILES_DIR

    def test_inpgen_from_string(self):
        """
        Test that the inpgen file is correctly parsed with teh from_str method of Structure
        """

        with open(TEST_FILES_DIR / "inp_test", "r", encoding="utf8") as f:
            content = f.read()

        s = Structure.from_str(content, fmt="fleur-inpgen")

        param = 5.130606429
        lattice = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]

        self.assertArrayAlmostEqual(lattice, s.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in s])
        self.assertArrayAlmostEqual(fraccoords, [site.frac_coords.tolist() for site in s])

    def test_fleur_xml_from_string(self):
        """
        Test that the fleur xml file is correctly parsed with the from_str method of Structure
        """

        with open(TEST_FILES_DIR / "inp.xml", "rb") as f:
            content = f.read()

        s = Structure.from_str(content, fmt="fleur")

        param = 5.1306085
        lattice = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.125, 0.125, 0.125], [-0.125, -0.125, -0.125]]

        self.assertArrayAlmostEqual(lattice, s.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in s])
        self.assertArrayAlmostEqual(fraccoords, [site.frac_coords.tolist() for site in s])

    def test_structure_to_inpgen_str(self):
        """
        Test that the to method of Structure produces the right output for the inpgen format
        """

        param = 5.130606429
        cell = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]

        struc = Structure(Lattice(cell), atoms, fraccoords)

        expected_inpgen_content = """\
        Si2
&input  cartesian=F /
       0.000000000        5.130606429        5.130606429
       5.130606429        0.000000000        5.130606429
       5.130606429        5.130606429        0.000000000
      1.0000000000
       1.000000000        1.000000000        1.000000000

      2
         14       0.0000000000       0.0000000000       0.0000000000
         14       0.2500000000       0.2500000000       0.2500000000
        """

        self.assertTrue(self.assertStrContentEqual(expected_inpgen_content, struc.to(fmt="fleur-inpgen")))

    def test_structure_from_file_inpgen(self):
        """
        Test that the from_file method reads the inpgen input correctly
        """

        s = Structure.from_file(TEST_FILES_DIR / "inp_test")

        param = 5.130606429
        lattice = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]

        self.assertArrayAlmostEqual(lattice, s.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in s])
        self.assertArrayAlmostEqual(fraccoords, [site.frac_coords.tolist() for site in s])

    def test_structure_from_file_inpgen_alternate_name(self):
        """
        Test that the from_file method reads the inpgen input correctly
        """

        with open(TEST_FILES_DIR / "inp_test", "r", encoding="utf8") as f:
            content = f.read()

        with TemporaryDirectory() as td:
            with open(Path(td) / "aiida.in", "w", encoding="utf8") as f:
                f.write(content)
            s = Structure.from_file(Path(td) / "aiida.in")

        param = 5.130606429
        lattice = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]

        self.assertArrayAlmostEqual(lattice, s.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in s])
        self.assertArrayAlmostEqual(fraccoords, [site.frac_coords.tolist() for site in s])

    def test_structure_from_file_xml(self):
        """
        Test that the XML file from fleur is correctly read in with the from_file method
        """
        s = Structure.from_file(TEST_FILES_DIR / "inp.xml")

        param = 5.1306085
        lattice = [[0, param, param], [param, 0, param], [param, param, 0]]
        atoms = ["Si", "Si"]
        fraccoords = [[0.125, 0.125, 0.125], [-0.125, -0.125, -0.125]]

        self.assertArrayAlmostEqual(lattice, s.lattice.matrix.tolist())
        self.assertEqual(atoms, [site.specie.symbol for site in s])
        self.assertArrayAlmostEqual(fraccoords, [site.frac_coords.tolist() for site in s])
