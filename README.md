[![ci-cd](https://github.com/johnwslee/extrucal/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/johnwslee/extrucal/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/johnwslee/extrucal/branch/main/graph/badge.svg?token=YT37K0ESGF)](https://codecov.io/gh/johnwslee/extrucal)
[![Documentation Status](https://readthedocs.org/projects/extrucal/badge/?version=latest)](https://extrucal.readthedocs.io/en/latest/index.html)
![license status](https://img.shields.io/github/license/johnwslee/extrucal)

# extrucal

**Author:** John W.S. Lee

`extrucal` provides functions that calculate throughputs and screw RPMs for various types of extrusion processes. Theoretical throughputs can be calculated by using the screw geometry and the processing condition, whereas the throughputs required for extruded products(cable, tube, rod, and sheet) can be calculated by using the product geometry. Based on these calculated throughputs, `extrucal` functions can generate tables and plots that show the processing windows considering extruder size, line speed, and screw RPM.

A large portion of arguments for the functions are given the typical values. Some of the arguments for functions are as follows:
 screw size, channel depth, polymer melt density, screw RPM, screw pitch, flight width, number of flights, line speed, extruder size, etc.

## Installation

`extrucal` can be installed PyPI using the following terminal command:

```bash
$ pip install extrucal
```

## Package Functions

**1. Functions in `extrucal.extrusion`**

- `throughput_cal()`
  - This function calculates the extrusion throughput (Drag Flow) given the screw size, RPM, the channel depth of metering channel, and screw pitch
  
- `throughput_table()`
  - This function generates a table containing the extrusion throughput with respect to channel depth and screw RPM
  
- `throughput_plot()`
  - This function generates a plot containing the extrusion throughput with respect to channel depth and screw RPM

**2. Functions in `extrucal.cable_extrusion`**

- `cable_cal()`
  - This function calculates the required throughput for cables given the outer diameter, thickness, line speed, and solid polymer density
  
- `cable_table()`
  - This function generate a table containing the required screw RPM with respect to line speed and extruder size
  
- `cable_plot()`
  - This function generate a plot containing the required screw RPM with respect to line speed and extruder size

**3. Functions in `extrucal.tube_extrusion`**

- `tube_cal()`
  - This function calculates the required throughput for tubes given the outer diameter, inner diameter, line speed, and solid polymer density
  
- `tube_table()`
  - This function generate a table containing the required screw RPM with respect to line speed and extruder size
  
- `tube_plot()`
  - This function generate a plot containing the required screw RPM with respect to line speed and extruder size

**4. Functions in `extrucal.rod_extrusion`**

- `rod_cal()`
  - This function calculates the required throughput for rods given the outer diameter, line speed, solid polymer density, and number of die holes
  
- `rod_table()`
  - This function generate a table containing the required screw RPM with respect to line speed and extruder size
  
- `rod_plot()`
  - This function generate a plot containing the required screw RPM with respect to line speed and extruder size

**5. Functions in `extrucal.sheet_extrusion`**

- `sheet_cal()`
  - This function calculates the required throughput for sheets given the width, thickness, line speed, solid polymer density, and number of die holes
  
- `sheet_table()`
  - This function generate a table containing the required screw RPM with respect to line speed and extruder size
  
- `sheet_plot()`
  - This function generate a plot containing the required screw RPM with respect to line speed and extruder size


## Usage

`extrucal` can be used to calculate extrusion throughput and to generate tables and plots of various parameters in extrusion processes

```python
from extrucal.extrusion import throughput_cal, throughput_table, throughput_plot
from extrucal.cable_extrusion import cable_cal, cable_table, cable_plot
from extrucal.tube_extrusion import tube_cal, tube_table, tube_plot
from extrucal.rod_extrusion import rod_cal, rod_table, rod_plot
from extrucal.sheet_extrusion import sheet_cal, sheet_table, sheet_plot
```

## Dependencies

-   Python 3.9 and Python packages:

    -   pandas==1.4.1
    -   numpy==1.22.2
    -   ipykernel==6.9.1
    -   altair-saver==0.5.0

## Documentation

Documentation `extrucal` can be found at [Read the Docs](https://extrucal.readthedocs.io/en/latest/index.html)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`extrucal` was created by John Lee. It is licensed under the terms of the MIT license.

## Credits

`extrucal` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
