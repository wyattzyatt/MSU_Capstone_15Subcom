function [ReceivedCommand] = Subcom15_Communicate(SendCommand, TS)
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
% TS: 1 or 0, to determine whether the test system is connected or not, 1
% if connected
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
    if TS == 1 
        for k = 20
            Timer1 = tic();
            clear Timer1
        end
        Timer1 = tic();
    end
    Subcom15_BFSK(SendCommand, dt, F1, F2);
    ReceivedCommand = '';
else
    % BFSK IS FROM READING IN THE HYDROPHONE EVENTUALLY

    % Create an audio input object
    audioInput = audioDeviceReader('SampleRate', 48000, 'NumChannels', 1);
    audioData = audioInput();
    
    % Set up FFT parameters
    fftSize = 2048;
    spectrumSPL_old = zeros(1025, 1);
    
    % Calibration factor (adjust this based on your microphone and setup)
    calibrationFactor = 45; % For example, if your microphone reads 94 dB as 0 dB SPL

    % Compute the spectrum using FFT
    bfsk = abs(fft(audioData, fftSize));
    
    % Demodulate the Audio received
    ReceivedCommand = Subcom15_Demodulate(bfsk, F1, F2, fs);

    % Release the audio input object
    release(audioInput);
    if TS == 1 
       toc(Timer1); 
       % TODO Make a GUI that displays information
    end
end
end

