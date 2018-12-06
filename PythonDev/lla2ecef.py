def lla2ecef(lat, lon, alt, latlon_unit='deg', alt_unit='m', model='wgs84'):
    """
    Convert Latitude, Longitude, Altitude, to ECEF position
    
    Parameters
    ----------
    lat : {(N,)} array like latitude, unit specified by latlon_unit, default in deg
    lon : {(N,)} array like longitude, unit specified by latlon_unit, default in deg
    alt : {(N,)} array like altitude, unit specified by alt_unit, default in m
    
    Returns
    -------
    ecef : {(N,3)} array like ecef position, unit is the same as alt_unit
    """
    lat,N1 = _input_check_Nx1(lat)
    lon,N2 = _input_check_Nx1(lon)
    alt,N3 = _input_check_Nx1(alt)
    
    if( (N1!=N2) or (N2!=N3) or (N1!=N3) ):
        raise ValueError('Inputs are not of the same dimension')
    
    if(model=='wgs84'):
        Rew,Rns = earthrad(lat,lat_unit=latlon_unit)
    else:
        Rew = wgs84.a 
    
    if(latlon_unit=='deg'):
        lat = np.deg2rad(lat)
        lon = np.deg2rad(lon)
    
    x = (Rew + alt)*np.cos(lat)*np.cos(lon)
    y = (Rew + alt)*np.cos(lat)*np.sin(lon)
    z = ( (1-wgs84._ecc_sqrd)*Rew + alt )*np.sin(lat)
    
    ecef = np.vstack((x,y,z)).T

    if(N1==1):
        ecef = ecef.reshape(3)

    return ecef
