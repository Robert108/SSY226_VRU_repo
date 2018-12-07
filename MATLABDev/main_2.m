earth = referenceSphere('Earth');

pos_initalized = false;
t0             = s.ALLsens(1,2);
t_prev         = s.ALLsens(1,2);
lastGyrData    = zeros(1,3);
nx             = 4; % Assuming that you use q as state variable in orient filter
y = 0;
y_gps = 0;
y_acc = zeros([1, 3]);
xgps = zeros([2, 1]);
gps_data = [];
alpha = 0.9;
RC = 5;

  xv = 0; 
  xp = 0;
  yv = 0; 
  yp = 0;
  xa = 0;
  ya = 0;
  t0k = s.ALLsens(1,2);
  j = 0;
 
% Init State vector 
x = zeros([4 2]);

P = [2 0  0  0; 
     0  2 0  0; 
     0  0  1  0; 
     0  0  0  1];                  % Prior covariance 

Q = [0.5 0 0 0; 
     0 0.5 0 0; 
     0 0  0.5 0; 
     0 0  0 0.5];                    % Process noise


  % Saved quaterion filter states.
  qhat.x = ones(nx, 1);
  qhat.P = ones(nx, nx, 1);

for i = 2:length(s.ALLsens)
    
    Ydata = s.ALLsens(i,:);
    
    if Ydata(1) == 4 % GPS measurment. 
        if ~pos_initalized             
            ipos_lat  = Ydata(3);
            ipos_long = Ydata(4);
            ipos_alt  = Ydata(5);
            pos_initalized = true;
        end
        lla = Ydata(3:5);
        ecef = lla2ecef(lla);
        % Get new GPS pos
        [GPS_East, GPS_North, zUp] = ecef2enu(ecef(1), ecef(2), ecef(3), ...
                                              ipos_lat, ipos_long, ipos_alt, earth); % Origin at the first GPS position
         GPS_North = GPS_North + 8.644464733671408e+03;
         
         xgps = [xgps x(1:2,end)];
    end
    
    
    if Ydata(1) ~= 4 % IMU measurment. update pose
        
        if Ydata(1) == 1 % Acceleration meas
            t      = Ydata(2);
            dtAcc  = t - t_prev;
            dt    = t - t0;
            t_prev = t;
        else
            t     = Ydata(2); 
            dt    = t - t0;
            t0    = t;
        end
    
        [qhat, lastGyrData]  = OrientFilter(Ydata, qhat, lastGyrData, dt); % Update pose
        rotm = quat2rotm(qhat.x'); % Rotation matrix that rotates sensors to east-north-up direction. 
      
        if Ydata(1) == 1  % rotate acceleration measurment
%          y_acc = [y_acc; Ydata(3:5)];
           g_effect = rotm(:,:)*[0.02, 0.02, 9.7]';
           
           xyz_acc(1:3) = rotm(:,:)*Ydata(3:5)';   % Remove effect of pose on acc values
           
           % LP filter
           alpha = dtAcc / (RC + dtAcc);
           y = y_acc(end,:) + alpha * (xyz_acc(1:3) - y_acc(end,:));
          
           y_acc = [y_acc; y];
           
       elseif Ydata(1) == 3
           xyz_mag(1:3) = rotm(:,:)*Ydata(3:5)';
       end
    end
    
    if (Ydata(1) == 1 || Ydata(1) == 4) && i >= 1818 % Acc or GPS; Run Kalman loop
    
        j = j+1;
            tk     = Ydata(2); 
            dtk    = tk - t0k;
            t0k    = tk;
            
    % Calculate prediction
    A = [1 0 dtk 0;
         0 1 0   dtk;
         0 0 1   0; 
         0 0 0   1];
 
    hx = A*x(:,j);   
    P = A*P*A'+ Q;       
            
    if Ydata(1) == 1
         H = [1/dtk^2 0 1/dtk 0; 0 1/dtk^2 0 1/dtk];
%         H = [0 0 0 0; 0 0 0 0];
        R  = [1 0;
              0 1];
        y = xyz_acc(1:2)';
        vk = y-H*(hx-x(:,j));
    else 
        H = [1 0 0 0; 0 1 0 0];
        R  = [3 0;
              0 3];
        gps_data = [gps_data; [GPS_East GPS_North]]; 
       
        y = [GPS_East GPS_North]'; 
        vk = y-H*hx;
        
    end

    % Update
    S = H*P*H' + R;  % Calc the innovation covariance
    K = P*H'*inv(S); % Calc the Kalman gain
    
    x(:,j+1) = hx + K*vk; % Calc the update mean
    P = P - K*S*K'; % Calc the update covariance
    
    end
    
end

   figure()
   plot(x(2,:), x(1,:), '.') 
   hold on
   plot(xgps(2,:), xgps(1,:), 'rx', 'MarkerSize', 3)
   plot(gps_data(:,2), gps_data(:,1), 'ro', 'MarkerSize', 3)
   axis equal
   
%    % Plot GPS position      
%    subplot(122)
%    plot(GPS_East, GPS_North, '.')
%    axis equal