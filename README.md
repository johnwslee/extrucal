[![ci-cd](https://github.com/johnwslee/extrucal/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/johnwslee/extrucal/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/johnwslee/extrucal/branch/main/graph/badge.svg?token=YT37K0ESGF)](https://codecov.io/gh/johnwslee/extrucal)
[![Documentation Status](https://readthedocs.org/projects/extrucal/badge/?version=latest)](https://extrucal.readthedocs.io/en/latest/?badge=latest)

# extrucal

**Author:** John Lee

`extrucal` provides functions for calculating throughput in extrusion processes and for generating tables and plots for throughput with respect to screw RPM and channel depth in metering section.

A large portion of arguments for the functions were given the typical values. The arguments for functions are as follows:
 screw size, channel depth, polymer melt density, screw RPM, screw pitch, flight width, number of flights

## Installation

`extrucal` can be installed PyPI using the following terminal command:

```bash
$ pip install extrucal
```

## Package Functions

**1. functions in `extrucal.extrusion`**

- `throughput_cal()`
  - This function calculates the extrusion throughput (Drag Flow) given the screw size, RPM, the channel depth of metering channel, and screw pitch
  
- `throughput_table()`
  - This function generates a table containing the extrusion throughput with respect to channel depth and screw RPM
  
- `throughput_plot()`
  - This function generates a plot containing the extrusion throughput with respect to channel depth and screw RPM

**2. functions in `extrucal.cable_extrusion`**

- `req_throughput_cal()`
  - This function calculates the required throughput given the outer diameter, inner diameter, line speed, and solid polymer density
  
- `req_rpm_table()`
  - This function generate a table containing the required screw RPM with respect to line speed and extruder size
  
- `req_rpm_plot()`
  - This function generate a plot containing the required screw RPM with respect to line speed and extruder size

## Usage

`extrucal` can be used to calculate extrusion throughput and to generate tables and plots of various parameters in extrusion processes

```python
from extrucal.extrusion import throughput_cal, throughput_table, throughput_plot
from extrucal.cable_extrusion import req_throughput_cal, req_rpm_table, req_rpm_plot
```

## Dependencies

-   Python 3.9 and Python packages:

    -   pandas==1.4.1
    -   numpy==1.22.2
    -   ipykernel==6.9.1
    -   altair-saver==0.5.0

## Documentation

Documentation `extrucal` can be found at [Read the Docs](https://extrucal.readthedocs.io/)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`extrucal` was created by John Lee. It is licensed under the terms of the MIT license.

## Credits

`extrucal` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
