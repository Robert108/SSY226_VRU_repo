% Get measurments

[xhat, meas] = filterTemplate

%%  Calculate mean and variance

% Mean Accelerometer
m_acc = mean(meas.acc(:, ~any(isnan(meas.acc), 1)), 2);
% Mean Gyroscope
m_gyr = mean(meas.gyr(:, ~any(isnan(meas.gyr), 1)), 2);
% Mean Magnetometer
m_mag = mean(meas.mag(:, ~any(isnan(meas.mag), 1)), 2);

% Accelerometer
Var_acc  = cov(meas.acc(:, ~any(isnan(meas.acc), 1))'); %, 1, 2);
% Gyroscope
Var_gyr  = cov(meas.gyr(:, ~any(isnan(meas.gyr), 1))'); %, 1, 2);
% Magnetometer
Var_mag  = cov(meas.mag(:, ~any(isnan(meas.mag), 1))'); %, 1, 2);

%% Histogram

% Accelerometer
hold on; 
histogram(acc, 9.9:0.001:10.05);
p1 =  plot([m_acc(3)-3*sqrt(Var_acc3) m_acc(3)-3*sqrt(Var_acc3)], [0 3000]);
      plot([m_acc(3)+3*sqrt(Var_acc3) m_acc(3)+3*sqrt(Var_acc3)], [0 3000])
legend(p1, '3\sigma-level')   
title('Histogram: Accelerometer, Z-axis'); xlabel('Acceleration [m/s^2]')
set(gca, 'FontSize', 14);

% Gyro
figure(2)
hold on;
histogram((meas.gyr(1, ~any(isnan(meas.gyr), 1))),-0.006:0.0002:0.006);
    p1 = plot([m_gyr(1)-3*sqrt(Var_gyr(1)) m_gyr(1)-3*sqrt(Var_gyr(1))], [0 4000]);
    plot([m_gyr(1)+3*sqrt(Var_gyr(1)) m_gyr(1)+3*sqrt(Var_gyr(1))], [0 4000])
     legend(p1, '3\sigma-level')  
title('Histogram: Gyroscope, X-axis'); xlabel('Angular velocity [rad/s]')
set(gca, 'FontSize', 14);

% Magnetometer
figure(3)
hold on;
histogram((meas.mag(2, ~any(isnan(meas.mag), 1))),0:0.01:5)
    p1 = plot([m_mag(2)-3*sqrt(Var_mag(2)) m_mag(2)-3*sqrt(Var_mag(2))], [0 1200]);
    plot([m_mag(2)+3*sqrt(Var_mag(2)) m_mag(2)+3*sqrt(Var_mag(2))], [0 1200])
     legend(p1, '3\sigma-level'); xlabel('Magnetic field [\muT]')
title('Histogram: Magnetometer, Y-axis')
set(gca, 'FontSize', 14);

%% Plot measurement reading over time
% plot acc x-axis
AxisLabel = {'X-axis', 'Y-axis', 'Z-axis'};
TitleLabel = {'Accelerometer', 'Gyroscope', 'Magnetometer'};
    
    for j = 1:3
        figure(1)
        subplot(1,3,j) 
        plot(meas.t(1,:), meas.acc(j,:)); title(AxisLabel{j})
         set(gca, 'FontSize', 14); xlabel('time [s]'); ylabel('Acceleration [m/s^2]')
        figure(2)
        subplot(1,3,j) 
        plot(meas.t(1,:), meas.gyr(j,:)); title(AxisLabel{j})
        set(gca, 'FontSize', 14); xlabel('time [s]'); ylabel('Angular velocity [rad/s]')
        figure(3)
        subplot(1,3,j) 
        plot(meas.t(1,:), meas.mag(j,:)); title(AxisLabel{j})
        set(gca, 'FontSize', 14); xlabel('time [s]'); ylabel('Magnetic field [\muT]')
    end
    for i = 1:3
    figure(i); 
    suptitle(TitleLabel{i});    
    end

%% Plot Euler angels 

% Convert to euler
xHatEuler = quat2eul(xhat.x', 'ZYZ')';
GoogleEuler = quat2eul(meas.orient', 'XYZ')';

% X-axis
subplot(131); hold on
plot(xhat.t,xHatEuler(1,:), '-', 'LineWidth', 1.5)
plot(xhat.t,GoogleEuler(1,:), '-', 'LineWidth', 1.5)
% Make it look nice
title('X-axis')
xlabel('time [s]'); ylabel('Angle [rad]')
legend('Own', 'Google', 'Location', 'northwest')
set(gca, 'FontSize', 14)

% Y-axis
subplot(132); hold on
plot(xhat.t,xHatEuler(2,:), '-', 'LineWidth', 1.5)
plot(xhat.t,GoogleEuler(2,:), '-', 'LineWidth', 1.5)
% Make it look nice
title('Y-axis')
xlabel('time [s]'); ylabel('Angle [rad]')
legend('Own', 'Google', 'Location', 'northwest')
set(gca, 'FontSize', 14)

% Z-axis
subplot(133);
hold on
plot(xhat.t,xHatEuler(3,:), '-', 'LineWidth', 1.5)
plot(xhat.t,GoogleEuler(3,:), '-', 'LineWidth', 1.5)
% Make it look nice
title('Z-axis')
xlabel('time [s]'); ylabel('Angle [rad]')
legend('Own', 'Google', 'Location', 'northwest')
set(gca, 'FontSize', 14)






