% test Csv file in matlab
clear all

filename  = 'data_no_gps_3.csv';
fid = fopen(filename,'rt');
s.ALLsens = [];
GPS = [];
g = 9.82; % convert from g to m/s^2

while true
  thisline = fgetl(fid);
  if ~ischar(thisline); break; end  %end of file
    C = strsplit(thisline, ',');
    time_list = strsplit(cell2mat(C(2)), (':'));
    time = str2num(cell2mat(time_list(1)))* 3600 + str2num(cell2mat(time_list(2)))* 60 + str2num(cell2mat(time_list(3)));
    if C(1) == "ACC"
        temp = [1, time, str2num(cell2mat(C(3)))*g, str2num(cell2mat(C(4)))*g,str2num(cell2mat(C(5)))*g];
        s.ALLsens = [s.ALLsens; temp];
    elseif C(1) == "GYRO"
        temp = [2, time, str2num(cell2mat(C(3))), str2num(cell2mat(C(4))),str2num(cell2mat(C(5)))];
        s.ALLsens = [s.ALLsens; temp];
    elseif C(1) == "MAG"
        temp = [3, time, str2num(cell2mat(C(3))), str2num(cell2mat(C(4))),str2num(cell2mat(C(5)))];
        s.ALLsens = [s.ALLsens; temp];
    elseif C(1) == "GPS" 
        temp_lat  = convertGPS(str2num(cell2mat(C(4))));
        temp_long = convertGPS(str2num(cell2mat(C(3))));
        temp = [4, time,temp_lat , temp_long, str2num(cell2mat(C(5)))];
        GPS = [GPS; temp];
        s.ALLsens = [s.ALLsens; temp];
    end
  end
  fclose(fid);