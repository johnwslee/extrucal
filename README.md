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

- `throughput()`
  - This function calculates the extrusion throughput (Drag Flow) given the screw size, RPM, the channel depth of metering channel, and screw pitch
  
- `throughput_table()`
  - This function generates a table containing the extrusion throughput with respect to channel depth and screw RPM
  
- `throughput_plot()`
  - This function generates a plot containing the extrusion throughput with respect to channel depth and screw RPM

## Usage

`extrucal` can be used to calculate throughput in extrusion processes and to generate table and plot for throughput as a function of screw RPM and channel depth in the metering section of screw

```python
from extrucal.extrucal import throughput, throughput_table, throughput_plot
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
