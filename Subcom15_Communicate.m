function ReceivedCommand = Subcom15_Communicate(SendCommand, TS)
% --------------------------
% 15Subcom Capstone Project
% Communication Protocol
% Wyatt Weller
% 1/3/2024
% --------------------------
% This Script contains the basics for our communication system, and will
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
% 
% [ReceivedCommand] = Subcom15_Communicate(SendCommand, TS)
% 
% --------------------------

% -- Variables
fs = 48000; % Sampling frequency (samples per second)
dt = 1/fs; % seconds per sample
F1 = 4000; % Sine wave frequency (4k hertz)
F2 = 8000; % Sine wave frequency (8k hertz)

SendCommand = cell2mat(SendCommand);

if (~isempty(SendCommand))
    
    SendCommand = [1 0 1 SendCommand 1 0 1];

    [bfsk, t] = Subcom15_BFSK(SendCommand, dt, F1, F2);

    soundsc(bfsk, fs)

    ReceivedCommand = '';
else
    ReceivedCommand = Subcom15_Polling(bfsk, F1, F2, fs)'; %[0 0 0 0 0 0 0 0];
end
end

