function [ReceivedCommand] = Subcom15_Communicate(SendCommand, TS)
% --------------------------
% 15Subcom Capstone Project
% Communication Protocol
% Wyatt Weller
% 1/3/2024
% --------------------------
% This Script is the basics for our communication system, and will
% be treated as if it is the function being called and return the variables
% as if it was an immitation of our physical system sending and receiving
% commands and thus it will be taking a command as an input, and returning
% the same command as a return variable
% 
% Use Case:
% 
% SendCommand: The input binary array given to be sent
% ReceivedCommand: The output binary array returned from the receiving
% system
% TS: 1 or 0, to determine whether the test system is connected or not, 1
% if connected
% 
% [ReceivedCommand] = Subcom15_Communicate(SendCommand, TS)
% 
% --------------------------

if TS == 1 
   Timer1 tic();
end

if TS == 1 
   toc(Timer1); 
   % TODO Make a GUI that displays information
end

end

