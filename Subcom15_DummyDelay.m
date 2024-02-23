function [Output, DelayedTime] =  Subcom15_DummyDelay(Input, DelayTime, TS)
% --------------------------
% 15Subcom Capstone Project
% Dummy Delay
% Wyatt Weller
% 11/10/2023
% --------------------------
% This Script will be imitating the latency of our communication, and will
% be treated as if it is the function being called and return the variables
% as if it was an immitation of our physical system sending and receiving
% commands and thus it will be taking a command as an input, and returning
% the same command as a return variable
% 
% Use Case:
% 
% Input: The input binary array given from the Test System
% Output: The output binary array returned to the Test System
% DelayedTime: The time measured delayed at the closest to the pause
% possible
% TS: 1 or 0, to determine whether the test system is connected or not, 1
% if true
% 
% [Output, DelayedTime] = DummyDelay(Input, DelayTime, TS)
% 
% --------------------------

if TS == 1
    Timer = tic();
    pause(DelayTime/1000);
    DelayedTime = toc(Timer);
    clear Timer
end
Output = Input;