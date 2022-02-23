import pytest
import pandas as pd
import numpy as np
import altair as alt
from extrucal.extrusion import throughput_cal
from extrucal.cable_extrusion import sheet_cal, sheet_table, sheet_plot
alt.renderers.enable('html')

def test_input_data():
    """
    Check Errors raised when incorrect inputs are used
    Test cases:
      1. input types
      2. input values
    """
    # Test input types

    with pytest.raises(TypeError):
        sheet_cal("1000", 1, 1, 1000)
    with pytest.raises(TypeError):
        sheet_cal(1000, "1", 1, 1000)
    with pytest.raises(TypeError):
        sheet_cal(1000, 1, "1", 1000)
    with pytest.raises(TypeError):
        sheet_cal(1000, 1, 1, "1000")

    with pytest.raises(TypeError):
        sheet_table("1000", 1, 1000)
    with pytest.raises(TypeError):
        sheet_table(1000, "1", 1000)
    with pytest.raises(TypeError):
        sheet_table(1000, 1, "1000")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, density_ratio="0.85")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, min_l_speed="1")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, max_l_speed="10")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, delta_l_speed="1")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, min_size="20")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, max_size="100")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, delta_size="20")
    with pytest.raises(TypeError):
        sheet_table(1000, 1, 1000, depth_percent="0.05")

    with pytest.raises(TypeError):
        sheet_plot("1000", 1, 1000)
    with pytest.raises(TypeError):
        sheet_plot(1000, "1", 1000)
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, "1000")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, density_ratio="0.85")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, min_l_speed="1")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, max_l_speed="10")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, delta_l_speed="1")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, min_size="20")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, max_size="100")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, delta_size="20")
    with pytest.raises(TypeError):
        sheet_plot(1000, 1, 1000, depth_percent="0.05")

    # Test input values

    with pytest.raises(ValueError):
        sheet_cal(100, 1, 1, 299)
    with pytest.raises(ValueError):
        sheet_cal(1000, 1, 1, 3001)

    with pytest.raises(ValueError):
        sheet_table(1000, 1, 299)
    with pytest.raises(ValueError):
        sheet_table(1000, 1, 3001)
    with pytest.raises(ValueError):
        sheet_table(1000, 1, 1000, density_ratio=1.01)
    with pytest.raises(ValueError):
        sheet_table(1000, 1, 1000, density_ratio=0.49)
    with pytest.raises(ValueError):
        sheet_table(1000, 1, 1000, delta_l_speed=10)
    with pytest.raises(ValueError):
        sheet_table(1000, 1, 1000, delta_size=81)
    with pytest.raises(ValueError):
        sheet_table(1000, 1, 1000, depth_percent=0.009)
    with pytest.raises(ValueError):
        sheet_table(1000, 1, 1000, depth_percent=0.31)

    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 299)
    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 3001)
    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 1000, density_ratio=1.01)
    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 1000, density_ratio=0.49)
    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 1000, delta_l_speed=10)
    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 1000, delta_size=81)
    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 1000, depth_percent=0.009)
    with pytest.raises(ValueError):
        sheet_plot(1000, 1, 1000, depth_percent=0.31)

def test_output():
    """
    Check if the returned output is correct
    """
    # Test the output of throughput()
    
    expected1 = 30
    actual1 = sheet_cal(1000, 1, 0.5, 1000)
    assert actual1 == expected1, "Calculated Value is wrong!!!"
    
    expected2 = 27.313
    actual2 = sheet_cal(1000.473, 1.3, 0.5, 700)
    assert actual2 == expected2, "Calculated Value is wrong!!!"

    # Test the output of throughput_table()
    
    expected5 = 5
    actual5 = len(sheet_table(1000, 1, 1000))
    assert actual5 == expected5, "The number of rows doesn't match!!!"
    
    expected6 = 9
    actual6 = len(sheet_table(1000, 1, 1000, delta_size=10))
    assert actual6 == expected6, "The number of rows doesn't match!!!"
    
    expected8 = 10
    actual8 = len(sheet_table(1000, 1, 1000).columns)
    assert actual8 == expected8, "The number of columns doesn't match!!!"

    expected9 = 5
    actual9 = len(sheet_table(1000, 1, 1000, max_l_speed=5).columns)
    assert actual9 == expected9, "The number of columns doesn't match!!!"
    
    # Test the output of throughput_plot()
    
    test_plot = sheet_plot(1000, 1, 1000)
    assert str(type(test_plot)) == "<class 'altair.vegalite.v4.api.Chart'>"
    assert test_plot.encoding.x.shorthand == 'size', "'size' should be mapped to the x axis"
    assert test_plot.encoding.y.shorthand == 'rpm', "'rpm' should be mapped to the y axis"
    assert test_plot.mark == 'line', "mark should be a line"
    tooltip = "[Tooltip({\n  shorthand: 'size'\n}), Tooltip({\n  shorthand: 'speed'\n}), Tooltip({\n  shorthand: 'rpm'\n})]"
    assert str(sheet_plot(10, 2, 1000).encoding.tooltip) == tooltip
