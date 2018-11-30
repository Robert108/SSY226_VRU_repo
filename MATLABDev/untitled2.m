% Convert to plane 

% Convert from lla to ecef and then to enu 
lla = s.GPS(:,2:4);
ecef = lla2ecef(lla);
earth = referenceSphere('Earth');
[xEast, yNorth, zUp] = ecef2enu(ecef(:,1), ecef(:,2), ecef(:,3), ecef(1,1), ecef(1,2), ecef(1,3), earth);

% Initilazation for kalman filter 
x_0 = [xEast(1); yNorth(1)]; P_0 = [10 0; 0 10]; % Prior mean and covarinace
A = [1 0; 0 1]; Q = [1 0; 0 1];                % State transition and process noise
H = [1 0; 0 1]; R = [6 0; 0 6];                % Measurement model matrix and measurement noise covariance
Y = [xEast, yNorth]';

[x, P] = kalmanFilter(Y, x_0, P_0, A, Q, H, R);

plot(xEast, yNorth)
axis equal