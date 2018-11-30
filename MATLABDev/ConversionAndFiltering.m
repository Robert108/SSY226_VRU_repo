clc
% Convert to plane 

% Convert from lla to ecef and then to enu 
lla = s.GPS(:,2:4);
ecef = lla2ecef(lla);
earth = referenceSphere('Earth');
[xEast, yNorth, zUp] = ecef2enu(ecef(:,1), ecef(:,2), ecef(:,3), ecef(1,1), ecef(1,2), ecef(1,3), earth);

% Use acc, gyr, and mag to get delta x and delta y

[xhat, meas] = OrientFilter(s);

xHatEuler = quat2eul(xhat.x', 'XYZ')';
rotm = eul2rotm(xHatEuler', 'XYZ');


% Initilazation for kalman filter 
x_0 = [xEast(1); yNorth(1)]; P_0 = [10 0; 0 10]; % Prior mean and covarinace
A = [1 0; 0 1]; Q = [1 0; 0 1];                  % State transition and process noise
H = [1 0; 0 1]; R = [10 0; 0 10];                % Measurement model matrix and measurement noise covariance
Y = [xEast, yNorth]';

[X, P, ~, ~] = kalmanFilter(Y, x_0, P_0, A, Q, H, R);


% Plot 
subplot(121)
plot(xEast, yNorth)
axis equal
subplot(122)
plot(X(1,:), X(2,:))
axis equal