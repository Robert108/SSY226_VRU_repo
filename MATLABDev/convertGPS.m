% File to convert the GPS reading to the correct values

function return_value = convertGPS(inputGPS)
    degmin = inputGPS;
    temp_min = mod(degmin,100);
    return_value = floor(degmin / 100) + (temp_min / 60);
end