function RSSIData = bleRSSI(tempData)
%
% bleRSSI: Extract RSSI values from data packet.
%
% INPUT:    tempData - collection of data packets from experiment
%           RSSIData - array of extracted RSSI values
% OUTPUT:   [] - figure
%

posUUID = 3:34;
posMajor = 38;
posMinor = 41;
posTx = 44:46;
posRSSI = 49:51;

UUID = '525049494F5400000000000000000000';

filteredData = cell(length(tempData),1);
for i = 1:length(tempData)
    ind = find( tempData{i}(posUUID) == UUID);
    if length(ind) == length(UUID)
        filteredData{i,1} = tempData{i};
    end
end

filteredData = filteredData(~cellfun('isempty',filteredData));

% get RSSI values
RSSIData = zeros(length(filteredData),1);
for i = 1:length(filteredData)
    RSSIData(i,1) = str2double(filteredData{i,1}(posRSSI));
end

end