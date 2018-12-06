def ecef2enu(x: float, y: float, z: float,
             lat0: float, lon0: float, h0: float,
             ell: Ellipsoid = None, deg: bool = True) -> Tuple[float, float, float]:
    """
    input
    -----
    x,y,z  [meters] target ECEF location                             [0,Infinity)
    Observer: lat0, lon0, h0 (altitude, meters)
    ell    reference ellipsoid
    deg    degrees input/output  (False: radians in/out)
    output:
    -------
    e,n,u   East, North, Up [m]
    """
    x0, y0, z0 = geodetic2ecef(lat0, lon0, h0, ell, deg=deg)

    return uvw2enu(x - x0, y - y0, z - z0, lat0, lon0, deg=deg)




def geodetic2ecef(lat: float, lon: float, alt: float,
                  ell: Ellipsoid = None, deg: bool = True) -> Tuple[float, float, float]:
    """
    `geodetic2ecef` is a point transformation from Geodetic of specified ellipsoid (default WGS-84) to ECEF
    ## Inputs
    * lat, lon (degrees)
    * alt (altitude, meters)
    * ell    reference ellipsoid
    * deg    degrees input/output  (False: radians in/out)
    ## OutputS
     ECEF x,y,z (meters)
    """
    if ell is None:
        ell = Ellipsoid()

    if deg:
        lat = radians(lat)
        lon = radians(lon)

    with np.errstate(invalid='ignore'):
        # need np.any() to handle scalar and array cases
        if np.any((lat < -pi / 2) | (lat > pi / 2)):
            raise ValueError('-90 <= lat <= 90')

        if np.any((lon < -pi) | (lon > 2 * pi)):
            raise ValueError('-180 <= lat <= 360')

    # radius of curvature of the prime vertical section
    N = get_radius_normal(lat, ell)
    # Compute cartesian (geocentric) coordinates given  (curvilinear) geodetic
    # coordinates.
    x = (N + alt) * cos(lat) * cos(lon)
    y = (N + alt) * cos(lat) * sin(lon)
    z = (N * (ell.b / ell.a)**2 + alt) * sin(lat)

    return x, y, z


    def get_radius_normal(lat_radians: float, ell: Ellipsoid = None) -> float:
    """ Compute normal radius of planetary body"""
    if ell is None:
        ell = Ellipsoid()

    a = ell.a
    b = ell.b

    return a**2 / sqrt(a**2 * cos(lat_radians)**2 + b**2 * sin(lat_radians)**2)




    def uvw2enu(u: float, v: float, w: float,
            lat0: float, lon0: float, deg: bool = True) -> Tuple[float, float, float]:
    if deg:
        lat0 = radians(lat0)
        lon0 = radians(lon0)

    t = cos(lon0) * u + sin(lon0) * v
    East = -sin(lon0) * u + cos(lon0) * v
    Up = cos(lat0) * t + sin(lat0) * w
    North = -sin(lat0) * t + cos(lat0) * w

    return East, North, Up