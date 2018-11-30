function [x, P] = mu_m(x, P, mag, m0, Rm)
% Input 
% x = state prediction
% P = covarinace prediction
% mag = magnetometer measurement
% Rm = magnetometer noise covarinace
% m0 = nominal magnetic field
% Output 
% x = State update
% P = Covariance update

% Calculate prediction
hx = Qq(x)'*m0;   

% Get the Jacobians 
[Qq1, Qq2, Qq3, Qq4]  = dQqdq(x);
Hx = [Qq1'*m0, Qq2'*m0, Qq3'*m0, Qq4'*m0]; 

            
S = Hx*P*Hx' + Rm; % Calc the innovation covariance
K = P*Hx'*inv(S); % Calc the Kalman gain
            
x = x + K*(mag - hx); % Calc the update mean
            
P = P - K*S*K'; % Calc the update covariance


