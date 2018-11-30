earth = referenceSphere('Earth');

% dT = 0.01;                           % Sampling time
% x_0 = [GPS_East(1); GPS_North(1)];   % Prior mean
% P_0 = [10 0; 0 10];                  % Prior covariance
% A = [1 0; 0 1];                      % State transition 
% Q = [10 0; 0 10];                    % Process noise
% H = [1 0; 0 1; dT 0; 0 dT];                     % Measurement model matrix
% R = [10 0 0 0; 0 10 0 0; 0 0 10 0; 0 0 0 10];   % Measurement noise covariance
% Y = [GPS_East, GPS_North, IMU_east, IMU_north]';

pos_initalized = false;
t0             = s.ALLsens(1,2);
lastGyrData    = zeros(1,3);
nx             = 4; % Assuming that you use q as state variable.
 
  % Saved filter states.
  xhat.x = ones(nx, 1);
  xhat.P = ones(nx, nx, 1);
            
  xv = zeros(4,1); xp = zeros(4,1); 
  yv = zeros(4,1); yp = zeros(4,1);

for i = 1:length(s.ALLsens)
    
    Ydata = s.ALLsens(i,:);
    
    if Ydata(1) == 4 % GPS measurment. 
        if ~pos_initalized 
            ipos_long = Ydata(3);
            ipos_lat  = Ydata(4);
            ipos_alt  = Ydata(5);
            pos_initalized = true;
        end
        lla = Ydata (3:5);
        ecef = lla2ecef(lla);
        % Get new GPS pos
        [GPS_East, GPS_North, zUp] = ecef2enu(ecef(:,1), ecef(:,2), ecef(:,3), ...
                                              ipos_long, ipos_lat, ipos_alt, earth); % Origin at the first GPS position
        
        % Plot GPS position                     
        plot(GPS_East, GPS_North, '.')
        hold on
        axis equal 
    end
    
    
    if Ydata(1) ~= 4 % IMU measurment. update pose and/or dx-dy
        
        if Ydata(1) == 1 % Acceleration meas
            t      = Ydata(2)  
            dtAcc  = t - t_prev
            t_prev = t;
        else
            t     = Ydata(2) 
            dt    = t - t0
            t0    = t;
        end
    
        [xhat, lastGyrData]  = OrientFilter(Ydata, xhat, lastGyrData, dt); % Update pose
        rotm = quat2rotm(xhat.x'); % Might have todo some conversion to get absolute east-north direction. 
    
       if Ydata(1) == 1  % Update dx-dy with acceleration measurment
           xyz_acc(1:3) = rotm(:,:)*(Ydata(3:5)'-[0 0 9.82]');   % Remove effect of pose on acc values
                                                     % Should we remove g? -[0 0 9.8]
           xv = xv + dtAcc*xyz_acc(1);              
           yv = yv + dtAcc*xyz_acc(2);

           xp_dot = xp + dtAcc*xv + dtAcc^2/2*xyz_acc(1);
           yp_dot = yp + dtAcc*yv + dtAcc^2/2*xyz_acc(2);
           xp = xp_dot;
           yp = yp_dot;
       end
    
    end
    
%     if ~any(isnan(acc))  % Acc measurements are available and outlier free.
%         [X, P, ~, ~] = kalmanFilter(Y, x_0, P_0, A, Q, H, R);      
%         [x, P] = mu_normalizeQ(x, P);
%         
%     end
   
    
end




% figure()
% plot(xp,yp)

% % Initilazation for kalman filter 
% x_0 = [xEast(1); yNorth(1)]; P_0 = [10 0; 0 10]; % Prior mean and covarinace
% A = [1 0; 0 1]; Q = [1 0; 0 1];                  % State transition and process noise
% H = [1 0; 0 1]; R = [10 0; 0 10];                % Measurement model matrix and measurement noise covariance
% Y = [xEast, yNorth]';
% 
% [X, P, ~, ~] = kalmanFilter(Y, x_0, P_0, A, Q, H, R);
% 
% 
% % Plot 
% subplot(121)
% plot(xEast, yNorth)
% axis equal
% subplot(122)
% plot(X(1,:), X(2,:))
% axis equal