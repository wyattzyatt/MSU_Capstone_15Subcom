function [Output, DelayedTime] =  Subcom15_DummyDelay(Input, DelayTime)
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
% DelayTime: The ammount of delay to create (-1 for random) in miliseconds
% 
% Output = DummyDelay(Input, DelayTime)
% 
% --------------------------

Timer = tic();
pause(DelayTime/1000);
DelayedTime = toc(Timer);
Output = Input;