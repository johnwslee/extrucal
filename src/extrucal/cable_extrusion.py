import pandas as pd
import numpy as np
import altair as alt
from extrucal.extrusion import throughput_cal


def cable_cal(outer_d, thickness, l_speed, s_density):
    """
    Calculates the required throughput for cables given the outer diameter, 
    thickness, line speed, and solid polymer density
    
    Parameters
    ----------
    outer_d     : int or float
                  Outer diameter [mm]
    thickness   : int or float
                  Insulation thickness [mm]
    l_speed     : int or float
                  Line speed [mpm]
    s_density   : int or float
                  Solid density of polymeric material [kg/m^3]

    Returns
    -------
    throughput : float
                 required exturion throughput [kg/hr]
    Examples
    --------
    >>> cable_cal(outer_d=10, thickness=2, l_speed = 10, s_density=1000)
    """
    # Test input type
    if not isinstance(outer_d, int):
        if not isinstance(outer_d, float):
            raise TypeError("'outer_d' should be either integer or float")
    if not isinstance(thickness, int):
        if not isinstance(thickness, float):
            raise TypeError("'thickness' should be either integer or float")
    if not isinstance(l_speed, int):
        if not isinstance(l_speed, float):
            raise TypeError("'l_speed' should be either integer or float")
    if not isinstance(s_density, int):
        if not isinstance(s_density, float):
            raise TypeError("'s_density' should be either integer or float")
    
    # Test input value
    if thickness > outer_d/2:
        raise ValueError("Thickness can't be greater than radius")
    if s_density < 300:
        raise ValueError("This is not solid density for polymers. Too low!!")
    if s_density > 3000:
        raise ValueError("This is not solid density for polymers. Too high!!")

    # Calculate basic variables
    inner_d = outer_d - (2*thickness)
    outer_r = outer_d / 2
    inner_r = inner_d / 2
    insul_area = np.pi*((outer_r**2)-(inner_r**2)) / 1000000
    req_throughput = l_speed * insul_area * 60 * s_density
    
    return round(req_throughput, 3)
  

def cable_table(
    outer_d, thickness, s_density, density_ratio=0.85, min_l_speed=1, 
    max_l_speed=10, delta_l_speed=1, min_size=20, max_size=100, delta_size=20, 
    depth_percent=0.05
):
    """
    Generate a table containing the required screw RPM with respect to 
    line speed and extruder size

    Parameters
    ----------
    outer_d       : int or float
                    Outer diameter [mm]
    thickness     : int or float
                    Insulation thickness [mm]
    s_density     : int or float
                    Solid density of polymeric material [kg/m^3]
    density_ratio : int or float
                    Ratio b/w solid and melt density
    min_l_speed   : int or float
                    Minimum line speed for calculation [mm]
                    Default value is 1 (1mpm)
    max_l_speed   : int or float
                    Maximum line speed for calculation [mpm]
                    Default value is 10 (10mpm)
    delta_l_speed : int or float
                    Amount of increment in line speed for calculation [mpm]
                    Default value is 1 (1mpm)
    min_size      : int or float
                    Minimum extruder size for calculation [mm]
                    Default value is 20 (20mm)
    max_size      : int or float
                    Maximum extruder size for calculation [mm]
                    Default value is 100 (100mm)
    delta_size    : int or float
                    Amount of increment in extruder size for calculation [mm]
                    Default value is 20 (20mm)
    depth_percent : int or float
                    Percentage of the depth of metering channel compared to extruder size
                    Default value is 0.05
    
    Returns
    -------
    table : pandas.DataFrame
            dataframe containing the required screw RPM as a function of line speed and extruder size
    Examples
    --------
    >>> cable_table(outer_d=10, thickness=2, s_density=1000)
    """
    # Test input type
    if not isinstance(outer_d, int):
        if not isinstance(outer_d, float):
            raise TypeError("'outer_d' should be either integer or float")
    if not isinstance(thickness, int):
        if not isinstance(thickness, float):
            raise TypeError("'thickness' should be either integer or float")
    if not isinstance(s_density, int):
        if not isinstance(s_density, float):
            raise TypeError("'s_density' should be either integer or float")
    if not isinstance(density_ratio, int):
        if not isinstance(density_ratio, float):
            raise TypeError("'density_ratio' should be either integer or float")
    if not isinstance(min_l_speed, int):
        if not isinstance(min_l_speed, float):
            raise TypeError("'min_l_speed' should be either integer or float")
    if not isinstance(max_l_speed, int):
        if not isinstance(max_l_speed, float):
            raise TypeError("'max_l_speed' should be either integer or float")
    if not isinstance(delta_l_speed, int):
        if not isinstance(delta_l_speed, float):
            raise TypeError("'delta_l_speed' should be either integer or float")
    if not isinstance(min_size, int):
        if not isinstance(min_size, float):
            raise TypeError("'min_size' should be either integer or float")
    if not isinstance(max_size, int):
        if not isinstance(max_size, float):
            raise TypeError("'max_size' should be either integer or float")
    if not isinstance(delta_size, int):
        if not isinstance(delta_size, float):
            raise TypeError("'delta_size' should be either integer or float")
    if not isinstance(depth_percent, int):
        if not isinstance(depth_percent, float):
            raise TypeError("'depth_percent' should be either integer or float")

    # Test input value
    if thickness > outer_d/2:
        raise ValueError("Thickness can't be greater than radius")
    if s_density < 300:
        raise ValueError("This is not solid density for polymers. Too low!!")
    if s_density > 3000:
        raise ValueError("This is not solid density for polymers. Too high!!")
    if density_ratio > 1:
        raise ValueError("Melt density can't be greater than solid density")
    if density_ratio < 0.5:
        raise ValueError("Melt density is too low (<50% of solid density)")
    if delta_l_speed > max_l_speed-min_l_speed:
        raise ValueError("'delta_l_speed' can not be greater than 'max_l_speed - min_l_speed'")
    if delta_size > max_size-min_size:
        raise ValueError("'delta_size' can not be greater than 'max_size - min_size'")
    if depth_percent < 0.01:
        raise ValueError("Channel depth is too shallow(<1% of screw size) to be used for extrusion screw")
    if depth_percent > 0.3:
        raise ValueError("Channel depth is too deep(>30% of screw size) to be used for extrusion screw")

    # Generates table
    table = dict()
    rpm_list = list()
    l_speed = [round(i, 2) for i in np.arange(min_l_speed, max_l_speed+0.001, delta_l_speed)]
    size = [j for j in np.arange(min_size, max_size+0.1, delta_size)]
    size_title = [f"{k}mm Ext" for k in np.arange(min_size, max_size+0.1, delta_size)]
    for l in l_speed:
        for s in size:
            rpm_list.append(
              round(
                (cable_cal(outer_d, thickness, l, s_density)/
                throughput_cal(s, s*depth_percent, s_density*density_ratio)),
                2))
        table[f"{l}mpm"] = rpm_list
        rpm_list = []
    table_df = pd.DataFrame(table, index=size_title)
    
    return table_df


def cable_plot(
    outer_d, thickness, s_density, density_ratio=0.85, min_l_speed=1, 
    max_l_speed=10, delta_l_speed=1, min_size=20, max_size=100, delta_size=1, 
    depth_percent=0.05
):
    """
    Generate a plot containing the required screw RPM with respect to 
    line speed and extruder size

    Parameters
    ----------
    outer_d       : int or float
                    Outer diameter [mm]
    thickness     : int or float
                    Insulation thickness [mm]
    s_density     : int or float
                    Solid density of polymeric material [kg/m^3]
    density_ratio : int or float
                    Ratio b/w solid and melt density
    min_l_speed   : int or float
                    Minimum line speed for calculation [mm]
                    Default value is 0 (0mpm)
    max_l_speed   : int or float
                    Maximum line speed for calculation [mpm]
                    Default value is 10 (10mpm)
    delta_l_speed : int or float
                    Amount of increment in line speed for calculation [mpm]
                    Default value is 1 (1mpm)
    min_size      : int or float
                    Minimum extruder size for calculation [mm]
                    Default value is 20 (20mm)
    max_size      : int or float
                    Maximum extruder size for calculation [mm]
                    Default value is 100 (100mm)
    delta_size    : int or float
                    Amount of increment in extruder size for calculation [mm]
                    Default value is 5 (5mm)
    depth_percent : int or float
                    Percentage of the depth of metering channel compared to extruder size
                    Default value is 0.05
    
    Returns
    -------
    plot : altair.Chart object
           a line chart showing the required screw RPM as a function of line speed and extruder size

    Examples
    --------
    >>> cable_plot(outer_d=10, thickness=2, s_density=1000)
    """
    # Test input type
    if not isinstance(outer_d, int):
        if not isinstance(outer_d, float):
            raise TypeError("'outer_d' should be either integer or float")
    if not isinstance(thickness, int):
        if not isinstance(thickness, float):
            raise TypeError("'thickness' should be either integer or float")
    if not isinstance(s_density, int):
        if not isinstance(s_density, float):
            raise TypeError("'s_density' should be either integer or float")
    if not isinstance(density_ratio, int):
        if not isinstance(density_ratio, float):
            raise TypeError("'density_ratio' should be either integer or float")
    if not isinstance(min_l_speed, int):
        if not isinstance(min_l_speed, float):
            raise TypeError("'min_l_speed' should be either integer or float")
    if not isinstance(max_l_speed, int):
        if not isinstance(max_l_speed, float):
            raise TypeError("'max_l_speed' should be either integer or float")
    if not isinstance(delta_l_speed, int):
        if not isinstance(delta_l_speed, float):
            raise TypeError("'delta_l_speed' should be either integer or float")
    if not isinstance(min_size, int):
        if not isinstance(min_size, float):
            raise TypeError("'min_size' should be either integer or float")
    if not isinstance(max_size, int):
        if not isinstance(max_size, float):
            raise TypeError("'max_size' should be either integer or float")
    if not isinstance(delta_size, int):
        if not isinstance(delta_size, float):
            raise TypeError("'delta_size' should be either integer or float")
    if not isinstance(depth_percent, int):
        if not isinstance(depth_percent, float):
            raise TypeError("'depth_percent' should be either integer or float")

    # Test input value
    if thickness > outer_d/2:
        raise ValueError("Thickness can't be greater than radius")
    if s_density < 300:
        raise ValueError("This is not solid density for polymers. Too low!!")
    if s_density > 3000:
        raise ValueError("This is not solid density for polymers. Too high!!")
    if density_ratio > 1:
        raise ValueError("Melt density can't be greater than solid density")
    if density_ratio < 0.5:
        raise ValueError("Melt density is too low (<50% of solid density)")
    if delta_l_speed > max_l_speed-min_l_speed:
        raise ValueError("'delta_l_speed' can not be greater than 'max_l_speed - min_l_speed'")
    if delta_size > max_size-min_size:
        raise ValueError("'delta_size' can not be greater than 'max_size - min_size'")
    if depth_percent < 0.01:
        raise ValueError("Channel depth is too shallow(<1% of screw size) to be used for extrusion screw")
    if depth_percent > 0.3:
        raise ValueError("Channel depth is too deep(>30% of screw size) to be used for extrusion screw")

    # Generate table for plot
    table = dict()
    rpm_list = list()
    l_speed = [round(i, 2) for i in np.arange(min_l_speed, max_l_speed+0.001, delta_l_speed)]
    size = [j for j in np.arange(min_size, max_size+0.1, delta_size)]
    for l in l_speed:
        for s in size:
            rpm_list.append(cable_cal(outer_d, thickness, l, s_density)/
            throughput_cal(s, s*depth_percent, s_density*density_ratio))
        table[l] = rpm_list
        rpm_list = []
    table_df = pd.DataFrame(table, index=size)
    table_for_plot = table_df.reset_index()
    table_for_plot = table_for_plot.rename(columns={"index": "size"})
    table_for_plot = table_for_plot.melt(id_vars="size", var_name="speed", value_name="rpm")
    table_for_plot["speed"] = table_for_plot["speed"].astype('category')
    
    # Generate plot
    plot = alt.Chart(table_for_plot, title='Screw RPM vs Extruder Size & Line Speed').mark_line().encode(
        alt.X("size", title="Extruder Size", scale=alt.Scale(domain=(min_size, max_size))),
        alt.Y("rpm", title="Screw RPM"),
        alt.Color(
            "speed", title="Line Speed [mpm]", 
            sort=alt.EncodingSortField('rpm', op='mean', order='descending')
        ),
        tooltip=["size", "speed", "rpm"]
    ).configure_axis(
        labelFontSize=14, titleFontSize=16
    ).configure_legend(
        labelFontSize=16, titleFontSize=14
    ).configure_title(
        fontSize=18
    )
    return plot
