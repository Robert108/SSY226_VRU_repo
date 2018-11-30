function [xhat, lastGyrData] = OrientFilter(Ydata, xhat, lastGyrData, dT)
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
  
  % Add your filter settings here.
  R_acc = diag([0.0002, 0.0001 0.0002]);
  R_gyr = diag([0.000001008 0.000001109 0.000000666]);
  R_mag = diag([0.258 0.2442 0.2155]);
  
  
  g0 =   [0.1 0.1 9.9]';  % Taken from a measurement when the phone is flat 
  % Todo: Set g0 to some standard if calibration is nonexistent. 
  m0 = [0 sqrt(0^2 + 5^2) -53]'; 
  % Todo Calc m0 from the initial GPS position
  
  Lm = norm(m0);  % Set magnetic field vector length
  alpha_m = 0.05; % Set alpha for the magnetic AR filter
  magOut = false;
  
  T = dT; % Set delta time 
  
      x = xhat.x(:);
      P = xhat.P(:, :);
            
      % Acceleromter
      if Ydata(1) == 1 && 9 < norm(Ydata(3:5)) && norm(Ydata(3:5)) < 11 % Acc measurements are available 
        acc    = Ydata(3:5)'; 
        [x, P] = mu_g(x, P, acc, R_acc, g0);        
        [x, P] = mu_normalizeQ(x, P);
      end
      
      % Gyroscope
      if Ydata(1) == 2  % Gyr measurements are available 
        gyr    = Ydata(3:5)';       
        [x, P] = tu_qw(x, P, gyr, T, R_gyr);        
        [x, P] = mu_normalizeQ(x, P);
        lastGyrData = gyr;     
      else
        [x, P] = tu_qw(x, P, lastGyrData, T, R_gyr);
        [x, P] = mu_normalizeQ(x, P);
        gyr = NaN;
      end      
           
      % Magnetometer
      if Ydata(1) == 3  % Mag measurements are available 
        mag  = Ydata(3:5)';      
      Lm = (1-alpha_m)*Lm + alpha_m*norm(mag); % AR(1) filter
          if  Lm*0.98 < Lm && Lm < Lm*1.02
              magOut = false;
              Lm = Lm;
          else 
              magOut = true;
          end  
      else
          magOut = false;
          mag = NaN;
      end 
          
      if ~any(isnan(mag)) && ~magOut  % Mag measurements are available.
        [x, P] = mu_normalizeQ(x, P);
        [x, P] = mu_m(x, P, mag, m0, R_mag);
        [x, P] = mu_normalizeQ(x, P);
      end

      % Save estimates
      xhat.x(:) = x;
      xhat.P(:, :) = P;

end
