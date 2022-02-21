import pandas as pd
import numpy as np
import altair as alt


def throughput(size, depth, density, rpm=1, pitch=None, w_flight=None, n_flight=1):
    """
    Calculates the extrusion throughput (Drag Flow) given the screw size, RPM,
    the channel depth of metering channel, and screw pitch
    ----------
    size     : float
               Screw size [mm]
    depth    : float
               Channel depth of metering section [mm]
    density  : float
               Melt density of polymeric material [kg/m^3]
    rpm      : float
               Screw RPM
               Default value is 1 (throughput per unit rpm)
    pitch    : float
               Screw pitch [mm]
               If None, squared pitch (=1D) is used
    w_flight : float
               Flight width [mm]
               If None, 10% of screw size is used for flight width
    n_flight : int
               Number of flight [ea]
               Default value is 1 (single-flighted)

    Returns
    -------
    float : volumetric throughput per rpm [kg/hr-RPM]

    Examples
    --------
    >>> throughput(size=200, depth=10, density=800)
    """
    # Assign default values
    if pitch == None:
        pitch = size
    if w_flight == None:
        w_flight = size*0.1
    
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
    Generate a table containing the volumetric throughput with respect to 
    channel depth and screw RPM
    ----------
    size        : float
                  screw size [mm]
    density     : float
                  melt density of polymeric material [kg/m^3]
    pitch       : float
                  Screw pitch [mm]
                  If None, squared pitch (=1D) is used
    w_flight    : float
                  Flight width [mm]
                  If None, 10% of screw size is used for flight width
    n_flight    : int
                  Number of flight [ea]
                  Default value is 1 (single-flighted)
    min_depth   : float
                  minimum depth for calculation [mm]
                  If None, 2% of screw size is used for minimum depth
    max_depth   : float
                  maximum depth for calculation [mm]
                  If None, 9% of screw size is used for maximum depth
    delta_depth : float
                  the amount of increment in depth for calculation [mm]
                  If None, 1% of screw size is used for depth increment
    min_rpm     : float
                  minimum screw RPM for calculation [RPM]
                  Default value is 5 (5RPM)
    max_rpm     : float
                  maximum screw RPM for calculation [RPM]
                  Default value is 50 (50RPM)
    delta_rpm   : float
                  the amount of increment in RPM for calculation [RPM]
                  Default value is 5 (5RPM)

    Returns
    -------
    table : pandas.DataFrame
            dataframe containing the throughput as a function of channel depth and screw RPM

    Examples
    --------
    >>> output_table(size=200, density=800)
    """
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
    
    # Generates table
    table = dict()
    throughput_list = list()
    depth = [round(i, 2) for i in np.arange(min_depth, max_depth+0.1, delta_depth)]
    rpm = [j for j in np.arange(min_rpm, max_rpm+0.1, delta_rpm)]
    rpm_title = [f"rpm={k}" for k in np.arange(min_rpm, max_rpm+0.1, delta_rpm)]
    for d in depth:
        for r in rpm:
            throughput_list.append(throughput(size, d, density, r, pitch, w_flight, n_flight))
        table[f"depth={d}"] = throughput_list
        throughput_list = []
    table_df = pd.DataFrame(table, index=rpm_title)
    print(
        f"\n\033[1mThroughput[kg/hr] at {min_rpm}~{max_rpm}RPM for channel depths from {min_depth} to {max_depth}mm\033[0m\n"
    )
    return table_df


def throughput_plot(
    size, density, pitch=None, w_flight=None, n_flight=1, min_depth=None, 
    max_depth=None, delta_depth=None, min_rpm=0, max_rpm=50, delta_rpm=1
):
    """
    Generates a plot containing the volumetric throughput with respect to 
    channel depth and screw RPM
    ----------
    size        : float
                  screw size [mm]
    density     : float
                  melt density of polymeric material [kg/m^3]
    pitch       : float
                  Screw pitch [mm]
                  If None, squared pitch (=1D) is used
    w_flight    : float
                  Flight width [mm]
                  If None, 10% of screw size is used for flight width
    n_flight    : int
                  Number of flight [ea]
                  Default value is 1 (single-flighted)
    min_depth   : float
                  minimum depth for calculation [mm]
                  If None, 2% of screw size is used for minimum depth
    max_depth   : float
                  maximum depth for calculation [mm]
                  If None, 9% of screw size is used for maximum depth
    delta_depth : float
                  the amount of increment in depth for calculation [mm]
                  If None, 1% of screw size is used for depth increment
    min_rpm     : float
                  minimum screw RPM for calculation [RPM]
                  Default value is 0 (0RPM)
    max_rpm     : float
                  maximum screw RPM for calculation [RPM]
                  Default value is 50 (50RPM)
    delta_rpm   : float
                  the amount of increment in RPM for calculation [RPM]
                  Default value is 1 (1RPM)

    Returns
    -------
    plot : altair.Chart object
           a line chart showing the throughput as a function of channel depth and screw RPM

    Examples
    --------
    >>> output_plot(size=200, density=800)
    """
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
    
    # Generate table for plot
    table = dict()
    throughput_list = list()
    depth = [round(i, 2) for i in np.arange(min_depth, max_depth+0.1, delta_depth)]
    rpm = [j for j in np.arange(min_rpm, max_rpm+0.1, delta_rpm)]
    for d in depth:
        for r in rpm:
            throughput_list.append(throughput(size, d, density, r, pitch, w_flight, n_flight))
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