function [x, P] = tu_qw(x, P, omega, T, Rw)

% Inputs
% x - last state
% P - last Covariance
% omega - measured angular rate
% T - the time since the last measurement
% Rw - the process noise covariance matrix
% Outputs
% x - updated step
% P - Updated covariance

% Calc matrices A and B
A = eye(4,4)+T/2*(Somega(omega));
B = (T/2)*Sq(x);

% Calculate prediction mean and Covariance. 
x = Ax;
P = A*P*A' + B*Rw*B';


end