import numpy as np

def  mu_g(x, P, yacc, Ra, g0):
    '''
    % Input
    % x = state prediction
    % P = covarinace prediction
    % yacc = accelerometer measurement
    % Ra = accelerometer noise covarinace
    % g0 = nominal gravity vector
    % Output
    % x = State update
    % P = Covariance update '''

    # Get the prediction
    hx = np.transpose(Qq(x))*g0

    # Get the Jacobians
    [Qq1, Qq2, Qq3, Qq4] = dQqdq(x)
    Hx = [np.transpose(Qq1)*g0, np.transpose(Qq2)*g0, np.transpose(Qq3)*g0, np.transpose(Qq4) * g0]

    S = Hx * P * np.transpose(Hx) + Ra # Calc the innovation covariance
    K = P * np.transpose(Hx)*np.linalg.inv(S) # Calc the Kalman gain

    x = x + K * (yacc - hx) # Calc the update mean

    P = P - K * S * np.transpose(K) # Calc the update covariance

    return x, P





