function [xhat, meas] = OrientFilter(Ydata)
% FILTERTEMPLATE  Filter template
%
% This is a template function for how to collect and filter data
% sent from a smartphone live.  Calibration data for the
% accelerometer, gyroscope and magnetometer assumed available as
% structs with fields m (mean) and R (variance).
%
% The function returns xhat as an array of structs comprising t
% (timestamp), x (state), and P (state covariance) for each
% timestamp, and meas an array of structs comprising t (timestamp),
% acc (accelerometer measurements), gyr (gyroscope measurements),
% mag (magnetometer measurements), and orint (orientation quaternions
% from the phone).  Measurements not availabe are marked with NaNs.
%
% As you implement your own orientation estimate, it will be
% visualized in a simple illustration.  If the orientation estimate
% is checked in the Sensor Fusion app, it will be displayed in a
% separate view.
%
% Note that it is not necessary to provide inputs (calAcc, calGyr, calMag).

  %% Filter settings
  t0 = [];  % Initial time (initialize on first data received)
  lastGyrData = zeros(1,3);
  nx = 4;   % Assuming that you use q as state variable.
  % Add your filter settings here.
  
  
  R_acc = diag([0.0002, 0.0001 0.0002]);
  R_gyr = diag([0.000001008 0.000001109 0.000000666]);
  R_mag = diag([0.258 0.2442 0.2155]);
  g0 =   [0.1 0.1 9.9]';          % Taken from a measurement when the phone is flat 
  %m0 = [0 sqrt(15.32^2 + 2.25^2) -15.16]'; % Taken from a measurement when the phone is flat for 70s. 
  m0 = [0 sqrt(0^2 + 5^2) -53]'; 
  
  Lm_prev = 53;
  alpha_m = 0.05;
  magOut = false;
  
  
  T = 0.01; % Set sampling frequency
  % Current filter state.
  x = [1; 0; 0 ;0];
  P = eye(nx, nx);

  % Saved filter states.
  xhat = struct('t', zeros(1, 0),...
                'x', zeros(nx, 0),...
                'P', zeros(nx, nx, 0));

  meas = struct('t', zeros(1, 0),...
                'acc', zeros(3, 0),...
                'gyr', zeros(3, 0),...
                'mag', zeros(3, 0),...
                'orient', zeros(4, 0));
       
            
for i = 2:max(size(Ydata.ACC))

      t = Ydata.ACC(i,1)/1000;  % Extract current time

      if isempty(t0)  % Initialize t0
        t0 = t;
      end
        
       % Accelerometer
       acc = Ydata.ACC(i,2:4)';
      if  9 < norm(acc) && norm(acc) < 11;
          accOut = false;
      else 
          accOut = true;
      end      
      
      if ~any(isnan(acc))  % Acc measurements are available and outlier free.
       
        [x, P] = mu_g(x, P, acc, R_acc, g0);        
        [x, P] = mu_normalizeQ(x, P);
        
      end
     

      
      if ~isempty(find(Ydata.GYR(:,1) ==  t*1000, 1))% Gyro measurements are available.
        % Do something        
        gyr = Ydata.GYR(i,2:4)';
        [x, P] = tu_qw(x, P, gyr, T, R_gyr);        
        [x, P] = mu_normalizeQ(x, P);
        lastGyrData = gyr;
      else
        gyr = NaN;
        [x, P] = tu_qw(x, P, lastGyrData, T, R_gyr);
        [x, P] = mu_normalizeQ(x, P);
      end      
            
      
      if ~isempty(find(Ydata.MAG(:,1) ==  t*1000,1))%  % Mag measurements are available.
           % Magnetometer 
          mag = Ydata.MAG(i,2:4)';
          
      else
          mag = NaN; 
      end
          if ~any(isnan(mag))
          Lm = (1-alpha_m)*Lm_prev + alpha_m*norm(mag); % AR(1) filter
              if  Lm_prev*0.98 < Lm && Lm < Lm_prev*1.02
                  magOut = false;
                  Lm_prev = Lm;
              else 
                  magOut = true;
              end  
          else
              magOut = false;
          end 
          
      if ~any(isnan(mag)) && ~magOut  % Mag measurements are available.
        [x, P] = mu_normalizeQ(x, P);
        [x, P] = mu_m(x, P, mag, m0, R_mag);
        [x, P] = mu_normalizeQ(x, P);
      end


      % Save estimates
      xhat.x(:, end+1) = x;
      xhat.P(:, :, end+1) = P;
      xhat.t(end+1) = t - t0;

      meas.t(end+1) = t - t0;
      meas.acc(:, end+1) = acc;
      meas.gyr(:, end+1) = gyr;
      meas.mag(:, end+1) = mag;
end

end
