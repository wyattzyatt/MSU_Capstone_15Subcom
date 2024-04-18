function ReceivedCommand = Subcom15_Communicate(SendCommand, messageLength)
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
    
    SendCommand = [1 0 1 SendCommand];

    [bfsk, ~] = Subcom15_BFSK(SendCommand, dt, F1, F2, messageLength);

    soundsc(bfsk, fs)

    ReceivedCommand = '';
else
    disp("Calling Polling")
    ReceivedCommand = Polling(fs, F1, F2, messageLength, 11)'; %[0 0 0 0 0 0 0 0];
    try 
        ReceivedCommand = ReceivedCommand(4:11);
    catch 
        ReceivedCommand = [0 0 0 0 0 0 0 0];
    end
    disp("Stopped Polling")
    disp(ReceivedCommand)
end
end

