filename = 'sensorLog_VRU_GPS_long_walk.txt';
[A,delimiterOut] = importdata(filename);

% Extract time 
start_time_ms = str2num(A.textdata{1});
time_ms = str2num(cell2mat(A.textdata(:,1))) - start_time_ms;

% Extract sensor types 
sensors_type = unique(A.textdata(:,2));
sensors_type = cell2mat(sensors_type); % covert to char matrix

% Store values for the different sensors
for i = 1:length(sensors_type)
    sens_type = sensors_type(i,:);
    ind = find(contains(A.textdata(:,2), sens_type));
    s.(sens_type) = [time_ms(ind) A.data(ind,:)];
end

