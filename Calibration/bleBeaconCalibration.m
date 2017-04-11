%% BLE Localization
% Calibration for RSSI
%
% ECSE 6964 - Internetworking of Things Final Project
% Mitchell Phillips, 661060944
% Chris V
%
% Last Updated: April 11, 2017
%

clc, clear, close all;

%% Import RSSI Data for each of the Beacons
%
% There are four beacons being used which all share the same UUID, but have
% different minor numbers. 
%
% Need to sift through data to get only beacons and info of interest.
%

for b = 1:4;

% beacon1
addpath('beacon1/');

 b1_d = cell(1,8);
 b1_RSSI_d = zeros(8,1);
% downscale
for i = 1:8;
    trial = num2str(5*i -1, '%02d');
    b1_d{:,i} = importdata(['b1_',trial,'in_d.txt']);
    b1_RSSI_d(i) = median(bleRSSI(b1_d{:,i}));
end
clear trial b1_d i

 b1_u = cell(1,8);
 b1_RSSI_u = zeros(8,1);
% upscale
for i = 1:8;
    trial = num2str(5*i -1, '%02u');
    b1_u{:,i} = importdata(['b1_',trial,'in_u.txt']);
    b1_RSSI_u(i) = median(bleRSSI(b1_u{:,i}));
end
clear trial b1_u

end



