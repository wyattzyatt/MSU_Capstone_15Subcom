% --------------------------
% 15Subcom Capstone Project
% Test System
% Wyatt Weller
% 11/10/2023
% --------------------------
% --------------------------
%close all; clear all; clc;

% Testing Parameters
MinTest = 0;
MaxTest = 2000;
TestInterval = 1;
NumberOfTests = 100;
TestRange = randi((MaxTest-MinTest)/TestInterval,NumberOfTests)*TestInterval + MinTest;%MinTest:TestInterval:MaxTest;
TestRange = TestRange(1,:);
TS = 1; % Test System connected

% Array Memory Pre-Allocation
Error = zeros(size(TestRange));
AvgError = zeros(size(TestRange));
TestTimes = zeros(size(TestRange));
TotalTimes = zeros(size(TestRange));
j=1;

% Testing/Timing
for i = TestRange
    Timer1 = tic();
    [Output,TestTimes(j)] = Subcom15_DummyDelay("10101010",i,TS);
    TotalTimes(j) = toc(Timer1);
    Error(j) = TotalTimes(j)-TestTimes(j);
    AvgError(j) =  sum(Error)/length(find(Error~=0));
    j=j+1;
end

% Plotting
figure(1);
subplot(211);
plot(1:length(Error),Error*1000);hold on;
plot(1:length(AvgError),AvgError*1000);hold off;
xlabel("Test Sample");
ylabel("Resulting Error (ms)");
legend("Error","Average Error");
subplot(212);
plot(1:length(TotalTimes),TotalTimes*1000);hold on;
plot(1:length(TestTimes),TestTimes*1000);hold off;
xlabel("Test Sample");
ylabel("Resulting Time (ms)");
legend("Total Time","Test Only Time");
disp(max(Error)*1000);

