import pandas as pd
import numpy as np
import altair as alt



def throughput_cal(size, depth, density, rpm=1, pitch=None, w_flight=None, n_flight=1):
    """
    Calculates the extrusion throughput (Drag Flow) given the screw size, RPM,
    the channel depth of metering channel, and screw pitch
    
    Parameters
    ----------
    size     : int or float
               Screw size [mm]
    depth    : int or float
               Channel depth of metering section [mm]
    density  : int or float
               Melt density of polymeric material [kg/m^3]
    rpm      : int or float
               Screw RPM
               Default value is 1 (throughput per unit rpm)
    pitch    : int or float
               Screw pitch [mm]
               If None, squared pitch (=1D) is used
    w_flight : int or float
               Flight width [mm]
               If None, 10% of screw size is used for flight width
    n_flight : int
               Number of flight [ea]
               Default value is 1 (single-flighted)

    Returns
    -------
    throughput : float
                 exturion throughput [kg/hr]

    Examples
    --------
    >>> throughput_cal(size=200, depth=10, density=800)
    """

    # Test input type
    if not isinstance(size, int):
        if not isinstance(size, float):
            raise TypeError("'size' should be either integer or float")
    if not isinstance(depth, int):
        if not isinstance(depth, float):
            raise TypeError("'depth' should be either integer or float")
    if not isinstance(density, int):
        if not isinstance(density, float):
            raise TypeError("'density' should be either integer or float")

    # Assign default values
    if pitch == None:
        pitch = size
    if w_flight == None:
        w_flight = size*0.1

    # Tests the types of default variables
    if not isinstance(rpm, int):
        if not isinstance(rpm, float):
            raise TypeError("'rpm' should be either integer or float")
    if not isinstance(pitch, int):
        if not isinstance(pitch, float):
            raise TypeError("'pitch' should be either integer or float")
    if not isinstance(w_flight, int):
        if not isinstance(w_flight, float):
            raise TypeError("'w_flight' should be either integer or float")
    if not isinstance(n_flight, int):
        raise TypeError("'n_flight' should be integer")

    # Test input value
    if depth < size*0.01:
        raise ValueError("Channel depth is too shallow(<1% of screw size) to be used for extrusion screw")
    if depth > size*0.3:
        raise ValueError("Channel depth is too deep(>30% of screw size) to be used for extrusion screw")
    if size < 5:
        raise ValueError("Screw size is too small!!")
    if size > 500:
        raise ValueError("Screw size is too big!!")
    if density < 300:
        raise ValueError("This is not melt density for polymers. Too low!!")
    if density > 3000:
        raise ValueError("This is not melt density for polymers. Too high!!")
    if pitch < size*0.2:
        raise ValueError("Screw pitch is too small")
    if pitch > size*2.5:
        raise ValueError("Screw pitch is too big")
    if w_flight < size*0.01:
        raise ValueError("Flight width is too small")
    if w_flight > size*0.7:
        raise ValueError("Flight width is too big")
    if n_flight not in [1, 2]:
        raise ValueError("You chose wrong value for n_flight. It should be either 1 or 2")

    # Calculate basic variables
    screw_root_size = size - (depth*2)
    helix_angle_b = np.arctan(pitch/(np.pi*size))
    helix_angle_c = np.arctan(pitch/(np.pi*screw_root_size))
    channel_width_b = ((pitch/n_flight)*np.cos(helix_angle_b))-w_flight
    channel_width_c = ((pitch/n_flight)*np.cos(helix_angle_c))-w_flight
    avg_channel_width = (channel_width_b + channel_width_c)/2
    
    # Generates table for shape factor (Drag)
    f_d_dict = dict()
    idx = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    for i in idx:
        f_d_dict[i] = (1/(i**3))*np.tanh((i*np.pi*depth)/(2*avg_channel_width))
    f_d_df = pd.Series(f_d_dict)
    
    # Calculation of basic variables continues
    shape_factor_drag = ((16*avg_channel_width)/(np.pi**3*depth))*f_d_df.sum()
    rotation_per_sec = rpm/60
    barrel_rot_speed = (np.pi*rotation_per_sec*size*np.cos(helix_angle_b))/1000
    throughput_per_sec = (
        n_flight*density*barrel_rot_speed*(
            avg_channel_width/1000)*(depth/1000)*shape_factor_drag
    ) / 2
    throughput_per_hr = throughput_per_sec * 60 * 60

    return round(throughput_per_hr, 2)


def throughput_table(
    size, density, pitch=None, w_flight=None, n_flight=1, min_depth=None, 
    max_depth=None, delta_depth=None, min_rpm=5, max_rpm=50, delta_rpm=5
):
    """
    Generate a table containing the extrusion throughput with respect to 
    channel depth and screw RPM
    
    Parameters
    ----------
    size        : int or float
                  Screw size [mm]
    density     : int or float
                  Melt density of polymeric material [kg/m^3]
    pitch       : int or float
                  Screw pitch [mm]
                  If None, squared pitch (=1D) is used
    w_flight    : int or float
                  Flight width [mm]
                  If None, 10% of screw size is used for flight width
    n_flight    : int
                  Number of flight [ea]
                  Default value is 1 (single-flighted)
    min_depth   : int or float
                  Minimum depth for calculation [mm]
                  If None, 2% of screw size is used for minimum depth
    max_depth   : int or float
                  Maximum depth for calculation [mm]
                  If None, 9% of screw size is used for maximum depth
    delta_depth : int or float
                  Amount of increment in depth for calculation [mm]
                  If None, 1% of screw size is used for depth increment
    min_rpm     : int or float
                  Minimum screw RPM for calculation [RPM]
                  Default value is 5 (5RPM)
    max_rpm     : int or float
                  Maximum screw RPM for calculation [RPM]
                  Default value is 50 (50RPM)
    delta_rpm   : int or float
                  Amount of increment in RPM for calculation [RPM]
                  Default value is 5 (5RPM)

    Returns
    -------
    table : pandas.DataFrame
            dataframe containing the throughput as a function of channel depth and screw RPM

    Examples
    --------
    >>> output_table(size=200, density=800)
    """

    # Test input type
    if not isinstance(size, int):
        if not isinstance(size, float):
            raise TypeError("'size' should be either integer or float")
    if not isinstance(density, int):
        if not isinstance(density, float):
            raise TypeError("'density' should be either integer or float")

    # Assign default values
    if pitch == None:
        pitch = size
    if w_flight == None:
        w_flight = size*0.1
    if min_depth == None:
        min_depth = size * 0.02
    if max_depth == None:
        max_depth = size * 0.09
    if delta_depth == None:
        delta_depth = size * 0.01

    # Tests the types of default variables
    if not isinstance(pitch, int):
        if not isinstance(pitch, float):
            raise TypeError("'pitch' should be either integer or float")
    if not isinstance(w_flight, int):
        if not isinstance(w_flight, float):
            raise TypeError("'w_flight' should be either integer or float")
    if not isinstance(n_flight, int):
        raise TypeError("'n_flight' should be integer")
    if not isinstance(min_depth, int):
        if not isinstance(min_depth, float):
            raise TypeError("'min_depth' should be either integer or float")
    if not isinstance(max_depth, int):
        if not isinstance(max_depth, float):
            raise TypeError("'max_depth' should be either integer or float")
    if not isinstance(delta_depth, int):
        if not isinstance(delta_depth, float):
            raise TypeError("'delta_depth' should be either integer or float")
    if not isinstance(min_rpm, int):
        if not isinstance(min_rpm, float):
            raise TypeError("'min_rpm' should be either integer or float")
    if not isinstance(max_rpm, int):
        if not isinstance(max_rpm, float):
            raise TypeError("'max_rpm' should be either integer or float")
    if not isinstance(delta_rpm, int):
        if not isinstance(delta_rpm, float):
            raise TypeError("'delta_rpm' should be either integer or float")

        # Test input value
    if min_depth < size*0.01:
        raise ValueError("Channel depth is too shallow(<1% of screw size) to be used for extrusion screw")
    if max_depth > size*0.3:
        raise ValueError("Channel depth is too deep(>30% of screw size) to be used for extrusion screw")
    if delta_depth > max_depth-min_depth:
        raise ValueError("'delta_depth' can not be greater than 'max_depth - min_depth'")
    if size < 5:
        raise ValueError("Screw size is too small!!")
    if size > 500:
        raise ValueError("Screw size is too big!!")
    if density < 300:
        raise ValueError("This is not melt density for polymers. Too low!!")
    if density > 3000:
        raise ValueError("This is not melt density for polymers. Too high!!")
    if pitch < size*0.2:
        raise ValueError("Screw pitch is too small")
    if pitch > size*2.5:
        raise ValueError("Screw pitch is too big")
    if w_flight < size*0.01:
        raise ValueError("Flight width is too small")
    if w_flight > size*0.7:
        raise ValueError("Flight width is too big")
    if n_flight not in [1, 2]:
        raise ValueError("You chose wrong value for n_flight. It should be either 1 or 2")

    # Generates table
    table = dict()
    throughput_list = list()
    depth = [round(i, 2) for i in np.arange(min_depth, max_depth+0.1, delta_depth)]
    rpm = [j for j in np.arange(min_rpm, max_rpm+0.1, delta_rpm)]
    rpm_title = [f"rpm={k}" for k in np.arange(min_rpm, max_rpm+0.1, delta_rpm)]
    for d in depth:
        for r in rpm:
            throughput_list.append(throughput_cal(size, d, density, r, pitch, w_flight, n_flight))
        table[f"depth={d}"] = throughput_list
        throughput_list = []
    table_df = pd.DataFrame(table, index=rpm_title)

    return table_df


def throughput_plot(
    size, density, pitch=None, w_flight=None, n_flight=1, min_depth=None, 
    max_depth=None, delta_depth=None, min_rpm=0, max_rpm=50, delta_rpm=1
):
    """
    Generates a plot containing the extrusion throughput with respect to 
    channel depth and screw RPM
    
    Parameters
    ----------
    size        : int or float
                  Screw size [mm]
    density     : int or float
                  Melt density of polymeric material [kg/m^3]
    pitch       : int or float
                  Screw pitch [mm]
                  If None, squared pitch (=1D) is used
    w_flight    : int or float
                  Flight width [mm]
                  If None, 10% of screw size is used for flight width
    n_flight    : int
                  Number of flight [ea]
                  Default value is 1 (single-flighted)
    min_depth   : int or float
                  Minimum depth for calculation [mm]
                  If None, 2% of screw size is used for minimum depth
    max_depth   : int or float
                  Maximum depth for calculation [mm]
                  If None, 9% of screw size is used for maximum depth
    delta_depth : int or float
                  Amount of increment in depth for calculation [mm]
                  If None, 1% of screw size is used for depth increment
    min_rpm     : int or float
                  Minimum screw RPM for calculation [RPM]
                  Default value is 0 (0RPM)
    max_rpm     : int or float
                  Maximum screw RPM for calculation [RPM]
                  Default value is 50 (50RPM)
    delta_rpm   : int or float
                  Amount of increment in RPM for calculation [RPM]
                  Default value is 1 (1RPM)

    Returns
    -------
    plot : altair.Chart object
           a line chart showing the throughput as a function of channel depth and screw RPM

    Examples
    --------
    >>> output_plot(size=200, density=800)
    """

    # Test input type
    if not isinstance(size, int):
        if not isinstance(size, float):
            raise TypeError("'size' should be either integer or float")
    if not isinstance(density, int):
        if not isinstance(density, float):
            raise TypeError("'density' should be either integer or float")

    # Assign default values
    if pitch == None:
        pitch = size
    if w_flight == None:
        w_flight = size*0.1
    if min_depth == None:
        min_depth = size * 0.02
    if max_depth == None:
        max_depth = size * 0.09
    if delta_depth == None:
        delta_depth = size * 0.01

    # Tests the types of default variables
    if not isinstance(pitch, int):
        if not isinstance(pitch, float):
            raise TypeError("'pitch' should be either integer or float")
    if not isinstance(w_flight, int):
        if not isinstance(w_flight, float):
            raise TypeError("'w_flight' should be either integer or float")
    if not isinstance(n_flight, int):
        raise TypeError("'n_flight' should be integer")
    if not isinstance(min_depth, int):
        if not isinstance(min_depth, float):
            raise TypeError("'min_depth' should be either integer or float")
    if not isinstance(max_depth, int):
        if not isinstance(max_depth, float):
            raise TypeError("'max_depth' should be either integer or float")
    if not isinstance(delta_depth, int):
        if not isinstance(delta_depth, float):
            raise TypeError("'delta_depth' should be either integer or float")
    if not isinstance(min_rpm, int):
        if not isinstance(min_rpm, float):
            raise TypeError("'min_rpm' should be either integer or float")
    if not isinstance(max_rpm, int):
        if not isinstance(max_rpm, float):
            raise TypeError("'max_rpm' should be either integer or float")
    if not isinstance(delta_rpm, int):
        if not isinstance(delta_rpm, float):
            raise TypeError("'delta_rpm' should be either integer or float")

    # Test input value
    if min_depth < size*0.01:
        raise ValueError("Channel depth is too shallow(<1% of screw size) to be used for extrusion screw")
    if max_depth > size*0.3:
        raise ValueError("Channel depth is too deep(>30% of screw size) to be used for extrusion screw")
    if delta_depth > max_depth-min_depth:
        raise ValueError("'delta_depth' can not be greater than 'max_depth - min_depth'")
    if size < 5:
        raise ValueError("Screw size is too small!!")
    if size > 500:
        raise ValueError("Screw size is too big!!")
    if density < 300:
        raise ValueError("This is not melt density for polymers. Too low!!")
    if density > 3000:
        raise ValueError("This is not melt density for polymers. Too high!!")
    if pitch < size*0.2:
        raise ValueError("Screw pitch is too small")
    if pitch > size*2.5:
        raise ValueError("Screw pitch is too big")
    if w_flight < size*0.01:
        raise ValueError("Flight width is too small")
    if w_flight > size*0.7:
        raise ValueError("Flight width is too big")
    if n_flight not in [1, 2]:
        raise ValueError("You chose wrong value for n_flight. It should be either 1 or 2")

    # Generate table for plot
    table = dict()
    throughput_list = list()
    depth = [round(i, 2) for i in np.arange(min_depth, max_depth+0.1, delta_depth)]
    rpm = [j for j in np.arange(min_rpm, max_rpm+0.1, delta_rpm)]
    for d in depth:
        for r in rpm:
            throughput_list.append(throughput_cal(size, d, density, r, pitch, w_flight, n_flight))
        table[d] = throughput_list
        throughput_list = []
    table_df = pd.DataFrame(table, index=rpm)
    table_for_plot = table_df.reset_index()
    table_for_plot = table_for_plot.rename(columns={"index": "RPM"})
    table_for_plot = table_for_plot.melt(id_vars="RPM", var_name="depth", value_name="throughput")
    table_for_plot["depth"] = table_for_plot["depth"].astype('category')
    
    # Generate plot
    plot = alt.Chart(table_for_plot, title='Throughput vs Screw RPM & Channel Depth').mark_circle().encode(
        alt.X("RPM", title="Screw RPM", scale=alt.Scale(domain=(0, max_rpm))),
        alt.Y("throughput", title="Throughput [kg/hr]"),
        alt.Color(
            "depth", title="Channel depth [mm]", 
            sort=alt.EncodingSortField('throughput', op='mean', order='descending')
        ),
        tooltip=["RPM", "depth", "throughput"]
    ).configure_axis(
        labelFontSize=14, titleFontSize=16
    ).configure_legend(
        labelFontSize=16, titleFontSize=14
    ).configure_title(
        fontSize=18
    )
    return plot
