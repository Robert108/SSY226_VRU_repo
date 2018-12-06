def earthrad(lat, lat_unit='deg', model='wgs84'):
    """
    Calculate radius of curvature in the prime vertical (East-West) and 
    meridian (North-South) at a given latitude.
    Parameters
    ----------
    lat : {(N,)} array like latitude, unit specified by lat_unit, default in deg
    
    Returns
    -------
    R_N : {(N,)} array like, radius of curvature in the prime vertical (East-West)
    R_M : {(N,)} array like, radius of curvature in the meridian (North-South)
    
    Examples
    --------
    >>> import numpy as np
    >>> from navpy import earthrad
    >>> lat = 0
    >>> Rtransverse, Rmeridian = earthrad(lat)
    >>> Rtransverse
    6378137.0
    >>> Rmeridian
    6335439.3272928288
    >>> lat = [0, np.pi/2]
    >>> Rtransverse, Rmeridian = earthrad(lat,lat_unit='rad')
    >>> Rtransverse
    array([ 6378137.        ,  6399593.62575849])
    >>> Rmeridian
    array([ 6335439.32729283,  6399593.62575849])
    """
    if(lat_unit=='deg'):
        lat = np.deg2rad(lat)
    elif(lat_unit=='rad'):
        pass
    else:
        raise ValueError('Input unit unknown')

    if(model=='wgs84'):
        R_N = wgs84.a/(1-wgs84._ecc_sqrd*np.sin(lat)**2)**0.5
        R_M = wgs84.a*(1-wgs84._ecc_sqrd)/(1-wgs84._ecc_sqrd*np.sin(lat)**2)**1.5
    else:
        raise ValueError('Model unknown')
    
    return R_N, R_M