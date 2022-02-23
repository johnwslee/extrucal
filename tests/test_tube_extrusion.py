import pytest
import pandas as pd
import numpy as np
import altair as alt
from extrucal.extrusion import throughput_cal
from extrucal.tube_extrusion import tube_cal, tube_table, tube_plot
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
        tube_cal("10", 6, 10, 1000)
    with pytest.raises(TypeError):
        tube_cal(10, "6", 10, 1000)
    with pytest.raises(TypeError):
        tube_cal(10, 6, "10", 1000)
    with pytest.raises(TypeError):
        tube_cal(10, 6, 10, "1000")

    with pytest.raises(TypeError):
        tube_table("10", 6, 1000)
    with pytest.raises(TypeError):
        tube_table(10, "6", 1000)
    with pytest.raises(TypeError):
        tube_table(10, 6, "1000")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, density_ratio="0.85")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, min_l_speed="1")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, max_l_speed="10")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, delta_l_speed="1")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, min_size="20")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, max_size="100")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, delta_size="20")
    with pytest.raises(TypeError):
        tube_table(10, 6, 1000, depth_percent="0.05")

    with pytest.raises(TypeError):
        tube_plot("10", 6, 1000)
    with pytest.raises(TypeError):
        tube_plot(10, "6", 1000)
    with pytest.raises(TypeError):
        tube_plot(10, 6, "1000")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, density_ratio="0.85")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, min_l_speed="1")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, max_l_speed="10")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, delta_l_speed="1")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, min_size="20")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, max_size="100")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, delta_size="20")
    with pytest.raises(TypeError):
        tube_plot(10, 6, 1000, depth_percent="0.05")

    # Test input values

    with pytest.raises(ValueError):
        tube_cal(10, 11, 10, 1000)
    with pytest.raises(ValueError):
        tube_cal(10, 6, 10, 299)
    with pytest.raises(ValueError):
        tube_cal(10, 6, 10, 3001)

    with pytest.raises(ValueError):
        tube_table(10, 11, 1000)
    with pytest.raises(ValueError):
        tube_table(10, 6, 299)
    with pytest.raises(ValueError):
        tube_table(10, 6, 3001)
    with pytest.raises(ValueError):
        tube_table(10, 6, 1000, density_ratio=1.01)
    with pytest.raises(ValueError):
        tube_table(10, 6, 1000, density_ratio=0.49)
    with pytest.raises(ValueError):
        tube_table(10, 6, 1000, delta_l_speed=10)
    with pytest.raises(ValueError):
        tube_table(10, 6, 1000, delta_size=81)
    with pytest.raises(ValueError):
        tube_table(10, 6, 1000, depth_percent=0.009)
    with pytest.raises(ValueError):
        tube_table(10, 6, 1000, depth_percent=0.31)

    with pytest.raises(ValueError):
        tube_plot(10, 11, 1000)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 299)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 3001)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 1000, density_ratio=1.01)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 1000, density_ratio=0.49)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 1000, delta_l_speed=10)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 1000, delta_size=81)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 1000, depth_percent=0.009)
    with pytest.raises(ValueError):
        tube_plot(10, 6, 1000, depth_percent=0.31)

def test_output():
    """
    Check if the returned output is correct
    """
    # Test the output of throughput()
    
    expected1 = 338.114
    actual1 = tube_cal(200, 150, 0.5, 820)
    assert actual1 == expected1, "Calculated Value is wrong!!!"
    
    expected2 = 430.675
    actual2 = tube_cal(250, 226, 1, 800)
    assert actual2 == expected2, "Calculated Value is wrong!!!"
    
    expected3 = 301.593
    actual3 = tube_cal(10, 6, 100, 1000)
    assert actual3 == expected3, "Calculated Value is wrong!!!"
    
    expected4 = 70.686
    actual4 = tube_cal(3, 2, 300, 1000)
    assert actual4 == expected4, "Calculated Value is wrong!!!"

    # Test the output of throughput_table()
    
    expected5 = 5
    actual5 = len(tube_table(10, 6, 1000))
    assert actual5 == expected5, "The number of rows doesn't match!!!"
    
    expected6 = 9
    actual6 = len(tube_table(10, 6, 1000, delta_size=10))
    assert actual6 == expected6, "The number of rows doesn't match!!!"
    
    expected8 = 10
    actual8 = len(tube_table(10, 6, 1000).columns)
    assert actual8 == expected8, "The number of columns doesn't match!!!"

    expected9 = 5
    actual9 = len(tube_table(10, 6, 1000, max_l_speed=5).columns)
    assert actual9 == expected9, "The number of columns doesn't match!!!"
    
    # Test the output of throughput_plot()
    
    test_plot = tube_plot(10, 6, 1000)
    assert str(type(test_plot)) == "<class 'altair.vegalite.v4.api.Chart'>"
    assert test_plot.encoding.x.shorthand == 'size', "'size' should be mapped to the x axis"
    assert test_plot.encoding.y.shorthand == 'rpm', "'rpm' should be mapped to the y axis"
    assert test_plot.mark == 'line', "mark should be a line"
    tooltip = "[Tooltip({\n  shorthand: 'size'\n}), Tooltip({\n  shorthand: 'speed'\n}), Tooltip({\n  shorthand: 'rpm'\n})]"
    assert str(tube_plot(10, 6, 1000).encoding.tooltip) == tooltip
