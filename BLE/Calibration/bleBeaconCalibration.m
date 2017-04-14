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
% In future just save data to CSV. Parcing data like this is wasteful.

RSSI_d = zeros(8,4); % downscale RSSI values
RSSI_u = zeros(8,4); % upscale RSSI values

for j = 1:4;
    
    b = num2str(j);
    %
    addpath(['beacon',b,'/']);
    
    b_d = cell(1,8);
    %b1_RSSI_d = zeros(8,1);
    % downscale
    for i = 1:8;
        trial = num2str(5*i -1, '%02d');
        b_d{:,i} = importdata(['b',b,'_',trial,'in_d.txt']);
        RSSI_d(i,j) = median(bleRSSI(b_d{:,i}));
    end
    clear i trial
    
    b_u = cell(1,8);
    %b1_RSSI_u = zeros(8,1);
    % upscale
    for i = 1:8;
        trial = num2str(5*i -1, '%02u');
        b_u{:,i} = importdata(['b',b,'_',trial,'in_u.txt']);
        RSSI_u(i,j) = median(bleRSSI(b_u{:,i}));
    end
    clear i trial b_d b_u
    
end

clear b j
%% Plot Up and DownScale for Each

dist = 4:5:39; % recorded measurement [in]
dist = dist.*0.0254; % recorded measurement [m]

figure(1);
C = {'k','b','r','g'};
for j = 1:4;
    plot(dist, RSSI_d(:,j),'-*','color',C{j})
    hold on
    plot(dist, RSSI_u(:,j),'--o','color',C{j})
end
clear j
legend('b1-upscale','b1-downscale','b2-upscale','b2-downscale',...
    'b3-upscale','b3-downscale','b4-upscale','b4-downscale')
title('Beacon: RSSI vs. Distance')
xlabel('Distance [m]')
ylabel('RSSI [dBm]')

%% Curve Fitting

% average RSSI values 
RSSI_avg = mean([mean(RSSI_u,2),mean(RSSI_d,2)],2);

% figure(3)
% loglog(dist, RSSI_avg, 'b*')
% p = polyfit
% hold on
% % [population2, gof] = fit( dist', RSSI_avg,  'poly1' );
% % plot( population2 )
% hold off

% parameter tuning
A = 62;
n = 1.40;
d = 0:0.01:1;
y = -(10*n)*log(d)-A;

figure(2)
plot(dist, RSSI_avg, 'b*')
hold on
plot(d,y,'r')
hold off
title('Average Beacon Reference')
xlabel('Distance [m]')
ylabel('RSSI [dBm]')
legend('Average Beacon RSSI', 'Reference Curve')