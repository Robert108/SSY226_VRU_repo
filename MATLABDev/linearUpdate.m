function [x, P, v_k, S] = linearUpdate(x, P, y, H, R)
%LINEARPREDICTION calculates mean and covariance of predicted state
%   density using a linear Gaussian model.
%
%Input:
%   x           [n x 1] Prior mean
%   P           [n x n] Prior covariance
%   y           [m x 1] Measurement
%   H           [m x n] Measurement model matrix
%   R           [m x m] Measurement noise covariance
%
%Output:
%   x           [n x 1] updated state mean
%   P           [n x n] updated state covariance
%

% Run Kalman filter update step 
%%%% State Update %%%%
v_k = y-H*x;
S = H*P*H'+R;
K_k = P*H'*inv(S);

x = x + K_k * v_k;
%%%% Covariance Update %%%%
P = P - K_k*S*K_k';
end