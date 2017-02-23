#!/usr/bin/env python


import numpy as np

from obspy.geodetics import calc_vincenty_inverse


def get_dist_in_km(station, event, obsd):
    """
    Returns distance in km
    """
    stats = obsd.stats
    station_coor = station.get_coordinates(".".join([stats.network,
                                                     stats.station,
                                                     stats.location,
                                                     stats.channel[:-1]+"Z"]))

    evlat = event.origins[0].latitude
    evlon = event.origins[0].longitude

    dist = calc_vincenty_inverse(station_coor["latitude"],
                                 station_coor["longitude"],
                                 evlat, evlon)[0] / 1000

    return dist


def get_time_array(obsd, event):
    stats = obsd.stats
    dt = stats.delta
    npts = stats.npts
    start = stats.starttime - event.origins[0].time
    return np.arange(start, start+npts*dt, dt)


def generate_user_levels(config, station, event, obsd, synt):
    """Returns a list of water levels
    """

    stats = obsd.stats
    npts = stats.npts

    base_water_level = config.stalta_waterlevel
    base_cc = config.cc_acceptance_level
    base_tshift = config.tshift_acceptance_level
    base_dlna = config.dlna_acceptance_level
    base_s2n = config.s2n_limit

    stalta_waterlevel = np.ones(npts)*base_water_level
    cc = np.ones(npts)*base_cc
    tshift = np.ones(npts)*base_tshift
    dlna = np.ones(npts)*base_dlna
    s2n = np.ones(npts)*base_s2n

    dist = get_dist_in_km(station, event, obsd)
    times = get_time_array(obsd, event)

    # Rayleigh
    # r_vel = 4.2
    # r_time = dist/r_vel
    # Love
    q_vel = 4.8
    q_time = dist/q_vel

    for i, time in enumerate(times):
        if time > dist/4.0 + 2*config.max_period:
            s2n[i] = 5*base_s2n
            cc[i] = 0.9
            stalta_waterlevel[i] *= 2
        if time < q_time:
            stalta_waterlevel[i] = 1

    return stalta_waterlevel, tshift, dlna, cc, s2n
