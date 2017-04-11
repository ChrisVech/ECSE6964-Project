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
% Need to sift through data to get only beacons of interest.
%

posUUID = 3:34;
posMajor = 38;
posMinor = 41;
posTx = 44:46;
posRSSI = 49:51;

UUID = '525049494F5400000000000000000000';

% beacon1
addpath('beacon1/');
b1_04in_d_temp = importdata('b1_04in_d.txt');
b1_04in_d = cell(length(b1_04in_d_temp),1);
for i = 1:length(b1_04in_d_temp)
    ind = find( b1_04in_d_temp{i}(posUUID) == UUID);
    if length(ind) == length(UUID)
        b1_04in_d{i,1} = b1_04in_d_temp{1};
    end
end
clear b1_04in_d_temp i

b1_04in_d = b1_04in_d(~cellfun('isempty',b1_04in_d));


% get RSSI values
for i = 1:length(b1_04in_d)
    b1_RSSI_04_d(i,1)
end