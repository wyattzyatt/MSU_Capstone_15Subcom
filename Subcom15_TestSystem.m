% --------------------------
% 15Subcom Capstone Project
% Test System
% Wyatt Weller
% 11/10/2023
% --------------------------
% --------------------------
%close all; clear all; clc;

% Testing Parameters
MinTest = 15;
MaxTest = 70;
TestInterval = 1;
NumberOfTests = 10000;
TestRange = randi((MaxTest-MinTest)/TestInterval,NumberOfTests)*TestInterval + MinTest;%MinTest:TestInterval:MaxTest;
TestRange = TestRange(1,:);
TS = 1; % Test System connected

% Array Memory Pre-Allocation
ErrorT = zeros(size(TestRange));
ErrorP = zeros(size(TestRange));
AvgErrorT = zeros(size(TestRange));
AvgErrorP = zeros(size(TestRange));
TestTimes = zeros(size(TestRange));
TotalTimes = zeros(size(TestRange));
j=1;

% Testing/Timing
for i = TestRange
    Timer1 = tic();
    [Output,TestTimes(j)] = Subcom15_DummyDelay("10101010",i,TS);
    TotalTimes(j) = toc(Timer1);
    if j>=10
%         AvgErrorT(j) =  sum(ErrorT(j-10:j))/10;%length(find(Error~=0));
%         AvgErrorP(j) =  sum(ErrorP(j-10:j))/10;
        ErrorT(j) = TotalTimes(j)-TestTimes(j);
        ErrorP(j) = ErrorT(j)/TestTimes(j);
        AvgErrorT(j) =  sum(ErrorT)/length(find(ErrorT~=0));
        AvgErrorP(j) =  sum(ErrorP)/length(find(ErrorP~=0));
    else
        AvgErrorT(j) =  sum(ErrorT)/length(find(ErrorT~=0));
        AvgErrorP(j) =  sum(ErrorP)/length(find(ErrorP~=0));
    end
    j=j+1;
    clear Timer1
    clear tic
    clear toc
end

% Plotting
figure(1);

subplot(311);
plot(10:length(ErrorT),ErrorT(10:end)*1000);hold on;
plot(10:length(AvgErrorT),AvgErrorT(10:end)*1000);hold off;
xlabel("Test Sample");
ylabel("Resulting Error (ms)");
legend("Error","Average Error");

subplot(312);
plot(10:length(ErrorP),ErrorP(10:end)*100);hold on;
plot(10:length(AvgErrorP),AvgErrorP(10:end)*100);hold off;
xlabel("Test Sample");
ylabel("Resulting Error (%)");
legend("Error","Average Error");

subplot(313);
plot(10:length(TotalTimes),TotalTimes(10:end)*1000);hold on;
plot(10:length(TestTimes),TestTimes(10:end)*1000);hold off;
xlabel("Test Sample");
ylabel("Resulting Time (ms)");
legend("Total Time","Test Only Time");
disp("Maximum Error(ms): "+max(ErrorT)*1000);
disp("Maximum Error(%):  "+max(ErrorP)*100);

% SEM = std(ErrorT)/sqrt(length(ErrorT));  
% ts = tinv([0.025  0.975],length(ErrorT)-1);    
% CI = mean(ErrorT) + ts*SEM;                 
% disp("With 90% Confidence the resulting error time is between " + CI(1)*1000 +" and " + CI(2)*1000 + "ms.");


% Calculate mean and standard deviation
mean_value = mean(ErrorT);
std_dev = std(ErrorT);

% Calculate the standard error of the mean (SEM)
sem = std_dev / sqrt(length(ErrorT));

% Set the desired confidence level (e.g., 99%)
confidence_level = 0.99;

% Calculate the critical value for the t-distribution
t_critical = tinv((1 + confidence_level) / 2, length(ErrorT) - 1);

% Calculate the margin of error
margin_of_error = t_critical * sem;

% Calculate the confidence interval
lower_bound = mean_value - margin_of_error;
upper_bound = mean_value + margin_of_error;

% Display the results
fprintf('Mean: %.4f\n', mean_value*1000);
fprintf('Standard Error of the Mean (SEM): %.4f\n', sem*1000);
fprintf('Critical Value for t-distribution: %.4f\n', t_critical);
fprintf('Margin of Error: %.4f\n', margin_of_error*1000);
fprintf('Confidence Interval(ms): [%.4f, %.4f]\n', lower_bound*1000, upper_bound*1000);

