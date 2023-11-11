% --------------------------
% 15Subcom Capstone Project
% Test System
% Wyatt Weller
% 11/10/2023
% --------------------------
% --------------------------
close all; clear all; clc;

% Testing Parameters
MaxTest = 1000;
MinTest = 500;
TestInterval = 15;
TestRange = MinTest:TestInterval:MaxTest;

% Array Memory Pre-Allocation
Error = zeros(size(TestRange));
AvgError = zeros(size(TestRange));
Output = zeros(size(TestRange));
TestTimes = zeros(size(TestRange));
TotalTimes = zeros(size(TestRange));
j=1;

% Testing/Timing
for i = TestRange
    Timer1 = tic();
    [Output(j),TestTimes(j)] = Subcom15_DummyDelay("10101010",i);
    TotalTimes(j) = toc(Timer1);
    Error(j) = TotalTimes(j)-TestTimes(j);
    AvgError(j) =  sum(Error)/length(find(Error~=0));
    j=j+1;
end

% Plotting
figure(1);
subplot(211);
plot(TestRange,Error*1000);hold on;
semilogy(TestRange,AvgError*1000);hold off;
xlabel("Testing Time (ms)")
ylabel("Resulting Error (ms)")
subplot(212);
plot(TestRange,TotalTimes*1000);hold on;
semilogy(TestRange,TestTimes*1000);hold off;
xlabel("Testing Time (ms)")
ylabel("Resulting Time (ms)")

