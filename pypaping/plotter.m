clear all
close all
clc

%% read the file output.txt
read_file = tdfread('output.txt');
fields_file =  fieldnames(read_file);
time = read_file.(fields_file{1,1});
min_ping = read_file.(fields_file{2,1});
max_ping = read_file.(fields_file{3,1});
avg_ping = read_file.(fields_file{4,1});

%% assign outputs to vars
% assign avg_pin_numbers to avg_ping_no
% assign time to xdate
for i = 1:length(avg_ping)
    min_ping_no(i,1) = str2double(min_ping(i,:));
    max_ping_no(i,1) = str2double(max_ping(i,:));
    avg_ping_no(i,1) = str2double(avg_ping(i,:));
end

if max(isnan(avg_ping_no))
    disp('There are some timeout values in this array!!!')
end

xdate = datenum(time,'yyyy/mm/dd HH:MM:SS');

%% plot the values
plot(xdate,[min_ping_no, max_ping_no, avg_ping_no],...
    'MarkerFaceColor',[0 0 0],'MarkerEdgeColor',[1 0 0],...
    'MarkerSize',2,...
    'Marker','o',...
    'LineWidth',2)
datetick('x','HHPM')
box on; grid on;
legend('Min Ping','Max Ping','Average Ping')
xlabel('Time')
ylabel('Pings in ms')
title(['Ping numbers for ' time(1,1:10)])