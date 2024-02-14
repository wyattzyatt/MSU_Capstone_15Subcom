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
    % if TS == 1 
    %     for k = 20
    %         Timer1 = tic();
    %         clear Timer1
    %     end
    %     Timer1 = tic();
    % end
    %Subcom15_BFSK(SendCommand, dt, F1, F2);
    ReceivedCommand = '';
else
    % BFSK IS FROM READING IN THE HYDROPHONE EVENTUALLY

    % Create an audiorecorder object
    recObj = audiorecorder(fs, 16, 1, 1); % 16-bit recording, mono channel

    % % Set up the figure for plotting
    % figure(48);
    % hPlot = plot(zeros(1024, 1));
    % title('Real-Time SPL Analysis');
    % xlabel('Frequency (Hz)');
    % ylabel('SPL (dB)');
    % grid on;
    % 
    % % Set up FFT parameters
    % fftSize = 2048;
    % spectrumSPL_old = zeros(1025, 1);
    % % Calibration factor (adjust this based on your microphone and setup)
    % calibrationFactor = 45; % For example, if your microphone reads 94 dB as 0 dB SPL
    % 
    % snippit = [2 2 2 2 2 2 2 2]
    % while (~isequal(snippit(1:3),[1 0 1]))
    %     % Set the sampling rate and duration of recording
    %     duration = 1; % Duration of recording in seconds
    % 
    %     % Record audio for the specified duration
    %     disp('Recording...');
    %     recordblocking(recObj, duration);
    %     pause(duration); % Wait for the recording to complete
    % 
    %     audioData = getaudiodata(recObj);
    % 
    %     snippit = Subcom15_Demodulate(audioData, F1, F2, fs)'
    % 
    %     % Compute the spectrum using FFT
    %     spectrum = abs(fft(audioData, fftSize));
    %     % Generate frequency axis
    %     frequencyAxis = linspace(0, fs/2, fftSize/2 + 1);
    %     % Compute SPL value
    %     spectrumSPL_new = 20*log10(spectrum(1:fftSize/2 + 1)) + calibrationFactor;
    %     spectrumSPL = (spectrumSPL_new + spectrumSPL_old)./2;
    %     spectrumSPL_old = spectrumSPL_new;
    % 
    %     % Update the plot
    %     set(hPlot, 'XData', frequencyAxis, 'YData', spectrumSPL);
    %     xlim([100, 16000]); % Set the x-axis limit to 100 Hz to 16 kHz
    %     ylim([-20, 100]); % Set the y-axis limit based on your expected SPL range
    % 
    %     drawnow;
    % end

    % Set the sampling rate and duration of recording
    %duration = 1; % Duration of recording in seconds
    
    % Record audio for the specified duration
    %recordblocking(recObj, duration);
    %pause(duration); % Wait for the recording to complete
    % disp('Recording stopped.');

    %bfsk = getaudiodata(recObj);

    ReceivedCommand = [1 1 1 1 1 1 1 1];%Subcom15_Demodulate(bfsk, F1, F2, fs)';

    % Release the audio input object
    % release(recObj);
    % if TS == 1 
    %    toc(Timer1); 
    %    % TODO Make a GUI that displays information
    % end
end
end

