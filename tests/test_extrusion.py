import pytest
import pandas as pd
import numpy as np
import altair as alt
from extrucal.extrusion import throughput_cal, throughput_table, throughput_plot
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
        throughput_cal("200", 10, 800)
    with pytest.raises(TypeError):
        throughput_cal(200, "10", 800)
    with pytest.raises(TypeError):
        throughput_cal(200, 10, "800")
    with pytest.raises(TypeError):
        throughput_cal(200, 10, 800, rpm="1")
    with pytest.raises(TypeError):
        throughput_cal(200, 10, 800, pitch="200")
    with pytest.raises(TypeError):
        throughput_cal(200, 10, 800, w_flight="20")
    with pytest.raises(TypeError):
        throughput_cal(200, 10, 800, n_flight=1.0)

    with pytest.raises(TypeError):
        throughput_table("200", 800)
    with pytest.raises(TypeError):
        throughput_table(200, "800")
    with pytest.raises(TypeError):
        throughput_table(200, 800, pitch="200")
    with pytest.raises(TypeError):
        throughput_table(200, 800, w_flight="20")
    with pytest.raises(TypeError):
        throughput_table(200, 800, n_flight=1.0)
    with pytest.raises(TypeError):
        throughput_table(200, 800, min_depth="4")
    with pytest.raises(TypeError):
        throughput_table(200, 800, max_depth="20")
    with pytest.raises(TypeError):
        throughput_table(200, 800, delta_depth="2")
    with pytest.raises(TypeError):
        throughput_table(200, 800, min_rpm="5")
    with pytest.raises(TypeError):
        throughput_table(200, 800, max_rpm="50")
    with pytest.raises(TypeError):
        throughput_table(200, 800, delta_rpm="5")

    with pytest.raises(TypeError):
        throughput_plot("200", 800)
    with pytest.raises(TypeError):
        throughput_plot(200, "800")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, pitch="200")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, w_flight="20")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, n_flight=1.0)
    with pytest.raises(TypeError):
        throughput_plot(200, 800, min_depth="4")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, max_depth="20")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, delta_depth="2")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, min_rpm="5")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, max_rpm="50")
    with pytest.raises(TypeError):
        throughput_plot(200, 800, delta_rpm="5")

    # Test input values
    
    with pytest.raises(ValueError):
        throughput_cal(200, 1, 800)
    with pytest.raises(ValueError):
        throughput_cal(200, 61, 800)
    with pytest.raises(ValueError):
        throughput_cal(4, 1, 800)
    with pytest.raises(ValueError):
        throughput_cal(501, 20, 800)
    with pytest.raises(ValueError):
        throughput_cal(200, 10, 290)
    with pytest.raises(ValueError):
        throughput_cal(200, 10, 3001)
    with pytest.raises(ValueError):
        throughput_cal(200, 10, 800, pitch=39)
    with pytest.raises(ValueError):
        throughput_cal(200, 10, 800, pitch=501)
    with pytest.raises(ValueError):
        throughput_cal(200, 10, 800, w_flight=1.9)
    with pytest.raises(ValueError):
        throughput_cal(200, 10, 800, w_flight=141)
    with pytest.raises(ValueError):
        throughput_cal(200, 10, 800, n_flight=3)

    with pytest.raises(ValueError):
        throughput_table(200, 800, min_depth = 1)
    with pytest.raises(ValueError):
        throughput_table(200, 800, max_depth = 61)
    with pytest.raises(ValueError):
        throughput_table(4, 800)
    with pytest.raises(ValueError):
        throughput_table(501, 800)
    with pytest.raises(ValueError):
        throughput_table(200, 290)
    with pytest.raises(ValueError):
        throughput_table(200, 3001)
    with pytest.raises(ValueError):
        throughput_table(200, 800, pitch=39)
    with pytest.raises(ValueError):
        throughput_table(200, 800, pitch=501)
    with pytest.raises(ValueError):
        throughput_table(200, 800, w_flight=1.9)
    with pytest.raises(ValueError):
        throughput_table(200, 800, w_flight=141)
    with pytest.raises(ValueError):
        throughput_table(200, 800, n_flight=3)
        
    with pytest.raises(ValueError):
        throughput_plot(200, 800, min_depth = 1)
    with pytest.raises(ValueError):
        throughput_plot(200, 800, max_depth = 61)
    with pytest.raises(ValueError):
        throughput_plot(4, 800)
    with pytest.raises(ValueError):
        throughput_plot(501, 800)
    with pytest.raises(ValueError):
        throughput_plot(200, 290)
    with pytest.raises(ValueError):
        throughput_plot(200, 3001)
    with pytest.raises(ValueError):
        throughput_plot(200, 800, pitch=39)
    with pytest.raises(ValueError):
        throughput_plot(200, 800, pitch=501)
    with pytest.raises(ValueError):
        throughput_plot(200, 800, w_flight=1.9)
    with pytest.raises(ValueError):
        throughput_plot(200, 800, w_flight=141)
    with pytest.raises(ValueError):
        throughput_plot(200, 800, n_flight=3)

def test_output():
    """
    Check if the returned output is correct
    """
    # Test the output of throughput()
    
    expected1 = 23.51
    actual1 = round(throughput_cal(200, 10, 800, rpm=1, pitch=200, w_flight=20, n_flight=1), 2)
    assert actual1 == expected1, "Calculated Value is wrong!!!"
    
    expected2 = 4540.04
    actual2 = round(throughput_cal(250, 12, 800, rpm=100, pitch=300, w_flight=25, n_flight=2), 2)
    assert actual2 == expected2, "Calculated Value is wrong!!!"
    
    expected3 = 1.69
    actual3 = round(throughput_cal(20, 2, 1000, rpm=30, pitch=20, w_flight=2, n_flight=1), 2)
    assert actual3 == expected3, "Calculated Value is wrong!!!"
    
    expected4 = 12.24
    actual4 = round(throughput_cal(150, 6.8, 800, rpm=1, pitch=206, w_flight=9, n_flight=1), 2)
    assert actual4 == expected4, "Calculated Value is wrong!!!"

    # Test the output of throughput_table()
    
    expected5 = 10
    actual5 = len(throughput_table(200, 1000))
    assert actual5 == expected5, "The number of rows doesn't match!!!"
    
    expected6 = 9
    actual6 = len(throughput_table(200, 1000, min_rpm=6))
    assert actual6 == expected6, "The number of rows doesn't match!!!"
    
    expected7 = 2
    actual7 = len(throughput_table(200, 1000, max_rpm=14))
    assert actual7 == expected7, "The number of rows doesn't match!!!"
    
    expected8 = 8
    actual8 = len(throughput_table(200, 1000).columns)
    assert actual8 == expected8, "The number of columns doesn't match!!!"

    expected9 = 3
    actual9 = len(throughput_table(200, 1000, max_depth=9).columns)
    assert actual9 == expected9, "The number of columns doesn't match!!!"
    
    expected10 = 2
    actual10 = len(throughput_table(200, 1000, min_depth=16).columns)
    assert actual10 == expected10, "The number of columns doesn't match!!!"
    
    # Test the output of throughput_plot()
    
    test_plot = throughput_plot(200, 1000)
    assert str(type(test_plot)) == "<class 'altair.vegalite.v4.api.Chart'>"
    assert test_plot.encoding.x.shorthand == 'RPM', "'RPM' should be mapped to the x axis"
    assert test_plot.encoding.y.shorthand == 'throughput', "'throughput' should be mapped to the y axis"
    assert test_plot.mark == 'circle', "mark should be a circle"
    tooltip = "[Tooltip({\n  shorthand: 'RPM'\n}), Tooltip({\n  shorthand: 'depth'\n}), Tooltip({\n  shorthand: 'throughput'\n})]"
    assert str(throughput_plot(200, 1000).encoding.tooltip) == tooltip
