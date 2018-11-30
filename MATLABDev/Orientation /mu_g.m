function [x, P] = mu_g(x, P, yacc, Ra, g0)

% Input 
% x = state prediction
% P = covarinace prediction
% yacc = accelerometer measurement
% Ra = accelerometer noise covarinace
% g0 = nominal gravity vector
% Output 
% x = State update
% P = Covariance update


% Get the prediction
hx = Qq(x)'*g0;          

% Get the Jacobians
[Qq1, Qq2, Qq3, Qq4]  = dQqdq(x);
Hx = [Qq1'*g0, Qq2'*g0, Qq3'*g0, Qq4'*g0]; 

            
S = Hx*P*Hx' + Ra; % Calc the innovation covariance
K = P*Hx'*inv(S); % Calc the Kalman gain
            
x = x + K*(yacc - hx); % Calc the update mean
            
P = P - K*S*K'; % Calc the update covariance
            
      


end





