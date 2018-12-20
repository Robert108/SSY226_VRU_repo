% test Csv file in matlab
clear all

filename  = 'data_no_gps_3.csv';
fid = fopen(filename,'rt');
s.ALLsens = []; % Struct 's' created with the field 'ALLsens' is created to store all sensor data
GPS = [];
g = 9.82; % convert from g to m/s^2

while true
  thisline = fgetl(fid); % Reading each line
  if ~ischar(thisline); break; end  % End of file
    C = strsplit(thisline, ','); % Reading characters until a ',' is encountered
    time_list = strsplit(cell2mat(C(2)), (':')); % Extracting the time, cell2mat converts cell array to ordinary arrays
    time = str2num(cell2mat(time_list(1)))* 3600 + str2num(cell2mat(time_list(2)))* 60 + str2num(cell2mat(time_list(3))); % Converting to seconds
    if C(1) == "ACC"
        temp = [1, time, str2num(cell2mat(C(3)))*g, str2num(cell2mat(C(4)))*g,str2num(cell2mat(C(5)))*g]; % Multiplying each acc value by g for m/s^2
        s.ALLsens = [s.ALLsens; temp]; % Appending to the struct 's'
    elseif C(1) == "GYRO"
        temp = [2, time, str2num(cell2mat(C(3))), str2num(cell2mat(C(4))),str2num(cell2mat(C(5)))]; % Same for gyro
        s.ALLsens = [s.ALLsens; temp];
    elseif C(1) == "MAG"
        temp = [3, time, str2num(cell2mat(C(3))), str2num(cell2mat(C(4))),str2num(cell2mat(C(5)))]; % Same for magnetometer
        s.ALLsens = [s.ALLsens; temp];
    elseif C(1) == "GPS" 
        temp_lat  = convertGPS(str2num(cell2mat(C(4)))); % Converting 'latitude' 
        temp_long = convertGPS(str2num(cell2mat(C(3)))); % Converting 'longitude' 
        temp = [4, time,temp_lat , temp_long, str2num(cell2mat(C(5)))]; 
        GPS = [GPS; temp]; 
        s.ALLsens = [s.ALLsens; temp]; % Appending to the struct 's'
    end
  end
  fclose(fid);
