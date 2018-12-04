earth = referenceSphere('Earth');

pos_initalized = false;
t0             = s.ALLsens(1,2);
t_prev         = s.ALLsens(1,2);
lastGyrData    = zeros(1,3);
nx             = 4; % Assuming that you use q as state variable in orient filter
y = 0;
y_gps = 0;
y_acc = [];
gps_data = [];
 
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

P = [100 0  0  0; 
     0  100 0  0; 
     0  0  20  0; 
     0  0  0  20];                  % Prior covariance 

Q = [200 0 0 0; 
     0 200 0 0; 
     0 0  50 0; 
     0 0  0 50];                    % Process noise


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
        rotm = quat2rotm(qhat.x'); % Might have todo some conversion to get absolute east-north direction. 
    
       if Ydata(1) == 1  % rotate acceleration measurment
%            y_acc = [y_acc; Ydata(3:5)];
           g_effect = rotm(:,:)*[0.02, 0.02, 9.7]';
           xyz_acc(1:3) = rotm(:,:)*Ydata(3:5)';   % Remove effect of pose on acc values
           
           y_acc = [y_acc; xyz_acc(1:3)];
       elseif Ydata(1) == 3
           xyz_mag(1:3) = rotm(:,:)*Ydata(3:5)';
       end
    end
    
    if (Ydata(1) == 1 || Ydata(1) == 4) && i >= 1000 % Acc or GPS; Run Kalman loop
    
        j = j+1;
            tk     = Ydata(2); 
            dtk    = tk - t0k;
            t0k    = tk;
            
    if Ydata(1) == 1
        H = [0 0 0 0; 0 0 0 0];
        R  = [0.5 0;
              0 0.5];
        y = xyz_acc(1:2)';
    else 
        H = [1 0 0 0; 0 1 0 0];
        R  = [10 0;
              0 10];
        gps_data = [gps_data; [GPS_East GPS_North]]; 
       
        y = [GPS_East GPS_North]'; 
    end
        
    % Calculate prediction
    A = [1 0 dtk 0;
         0 1 0   dtk;
         0 0 1   0; 
         0 0 0   1];
 
    hx = A*x(:,j);   
    P = A*P*A'+ Q;
    
    % Update
    vk = y-H*hx;
    S = H*P*H' + R;  % Calc the innovation covariance
    K = P*H'*inv(S); % Calc the Kalman gain
    
    x(:,j+1) = hx + K*vk; % Calc the update mean
    P = P - K*S*K'; % Calc the update covariance
    
    end
    
end

   figure()
   plot(x(1,:), x(2,:), '.')     
   hold on
   plot(gps_data(:,1), gps_data(:,2), 'ro', 'MarkerSize', 3)
   axis equal
   
%    % Plot GPS position      
%    subplot(122)
%    plot(GPS_East, GPS_North, '.')
%    axis equal