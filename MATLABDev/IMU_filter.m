function [rb] = IMU_filter(s)
% Function that outputs a filtered IMU poisition from a structure s 
% Input 
% 
% Output
%

[xhat, meas] = OrientFilter(s);
rotm = quat2rotm(xhat.x');
% Might have todo conversion to get absolute east-north direction. 

xv = zeros(length(rotm),1); xp = zeros(length(rotm),1); 
yv = zeros(length(rotm),1); yp = zeros(length(rotm),1);
T = 0.01;
for i = 1:length(rotm)-1
   xyz_acc(i,1) = s.ACC(i, 1); % Save time in new var
   xyz_acc(i,2:4) = rotm(:,:,i)*s.ACC(i, 2:4)';   % perform rotation matrix on acc values
                                                  % Should we remove g? -[0 0 9.8]
   xv(i+1) = xv(i) + T*xyz_acc(i,2);              
   yv(i+1) = yv(i) + T*xyz_acc(i,3);
   
   xp(i+1) = xp(i) + T*xv(i) + T^2/2*xyz_acc(i,2);
   yp(i+1) = yp(i) + T*yv(i) + T^2/2*xyz_acc(i,3);
end

rb = [xp, yp];





% Old Plot functions

% plot(xp, yp)
% subplot(131)
% hold on 
% plot(xyz_acc(:,4))
% plot(s.ACC(:, 4))
% legend('rotated','org')
% title('Z-axis')
% subplot(132)
% hold on 
% plot(xyz_acc(:,3))
% plot(s.ACC(:, 3))
% legend('rotated','org')
% title('Y-axis')
% subplot(133)
% hold on 
% plot(xyz_acc(:,2))
% plot(s.ACC(:, 2))
% legend('rotated','org')
% title('X-axis')