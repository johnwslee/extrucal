from extrucal.extrucal import throughput, throughput_table, throughput_plot
import pytest
import pandas as pd
import numpy as np
import altair as alt
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
        throughput("200", 10, 800)
    with pytest.raises(TypeError):
        throughput(200, "10", 800)
    with pytest.raises(TypeError):
        throughput(200, 10, "800")
    with pytest.raises(TypeError):
        throughput(200, 10, 800, rpm="1")
    with pytest.raises(TypeError):
        throughput(200, 10, 800, pitch="200")
    with pytest.raises(TypeError):
        throughput(200, 10, 800, w_flight="20")
    with pytest.raises(TypeError):
        throughput(200, 10, 800, n_flight=1.0)

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
        throughput(200, 1, 800)
    with pytest.raises(ValueError):
        throughput(200, 61, 800)
    with pytest.raises(ValueError):
        throughput(4, 1, 800)
    with pytest.raises(ValueError):
        throughput(501, 20, 800)
    with pytest.raises(ValueError):
        throughput(200, 10, 290)
    with pytest.raises(ValueError):
        throughput(200, 10, 3001)
    with pytest.raises(ValueError):
        throughput(200, 10, 800, pitch=39)
    with pytest.raises(ValueError):
        throughput(200, 10, 800, pitch=501)
    with pytest.raises(ValueError):
        throughput(200, 10, 800, w_flight=1.9)
    with pytest.raises(ValueError):
        throughput(200, 10, 800, w_flight=141)
    with pytest.raises(ValueError):
        throughput(200, 10, 800, n_flight=3)

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
    expected1 = 23.51
    actual1 = throughput(200, 10, 800, rpm=1, pitch=200, w_flight=20, n_flight=1)
    assert actual1 == expected1, "Calculated Value is wrong!!!"
    
    expected2 = 4540.04
    actual2 = throughput(250, 12, 800, rpm=100, pitch=300, w_flight=25, n_flight=2)
    assert actual2 == expected2, "Calculated Value is wrong!!!"
    
    expected3 = 1.69
    actual3 = throughput(20, 2, 1000, rpm=30, pitch=20, w_flight=2, n_flight=1)
    assert actual3 == expected3, "Calculated Value is wrong!!!"
    
    expected4 = 12.24
    actual4 = throughput(150, 6.8, 800, rpm=1, pitch=206, w_flight=9, n_flight=1)
    assert actual4 == expected4, "Calculated Value is wrong!!!"