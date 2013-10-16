"""Test the python scripts with subprocess.check_call

"""

from subprocess import check_call
import shutil
import os

test_folder = "data"
test_file = "data.hdf5"

class TestScripts(object):
    """Check that the scripts don't raise exceptions on normal operations.

    - make_hdf5.py
    - export_dataset.py
    - projection_stack.py
    - pitch.py
    - dpc_radiography.py
    - phase_drift.py
    - visibility_map.py
    - export_images.py
    - intensity_scan.py
    - ct_reconstruction.py
    """

    def test_make_hdf5(self):
        command = "make_hdf5.py --keep " + test_folder
        argument_sets = [
                "",
                "-o",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)

    def test_export_dataset(self):
        setup_command = "projection_stack.py -b " + test_file
        check_call(setup_command, shell=True)
        command = "export_dataset.py " + test_file
        argument_sets = [
                "",
                "-o --dataset postprocessing/stack_pixel_509",
                "-o",
                "-o --roi 150 950",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)
        os.remove("data_postprocessing_stack_pixel_509.tif")

    def test_projection_stack(self):
        command = "projection_stack.py " + test_file
        argument_sets = [
                "-b",
                "-b -o --pixel 511",
                "-b -o",
                "-b -o --roi 150 950",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)

    def test_pitch(self):
        command = "pitch.py test_pitch.hdf5"
        argument_sets = [
                "-b --pixel 516 --split 17",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)

    def test_dpc_radiography(self):
        command = "dpc_radiography.py -b --steps 6 {0} --flat {0}".format(
                test_file)
        argument_sets = [
                "",
                "-o",
                "-o --roi 400 700",
                "-o --roi 400 700 --periods 2",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)

    def test_phase_drift(self):
        command = "phase_drift.py -b {0}".format(test_file)
        argument_sets = [
                "--steps 3",
                "-o --steps 3",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)

    def test_visibility_map(self):
        command = "visibility_map.py -b {0}".format(test_file)
        argument_sets = [
                "--steps 3",
                "-o --steps 6",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)

    def test_export_images(self):
        command = "export_images.py " + test_file
        argument_sets = [
                "",
                "-o",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)
        shutil.rmtree("data/tif")

    def test_intensity_scan(self):
        command = "intensity_scan.py -b {0}".format(test_file)
        argument_sets = [
                "--roi 200 800 510 520",
                "--roi 500 550 509 511",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)

    def test_ct_reconstruction(self):
        command = "ct_reconstruction.py {0} -b --dataset postprocessing/absorption".format(
                test_file)
        argument_sets = [
                "--filter parzen",
                "-o --filter parzen",
                "--filter parzen --centre 10",
                ]
        for argument_set in argument_sets:
            full_command = command + " " + argument_set
            print(full_command)
            check_call(full_command, shell=True)
