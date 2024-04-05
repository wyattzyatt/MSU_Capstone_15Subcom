%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% RTA - audio test for transitter analysis
% Original Auther: Matlab Example Code
% Auther: Iain D. Scott
% 11/30/2023
%
% Description: This code performs the FFT on incoming
%              audio data, averages twice and displays
%              calibrated SPL level.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all; clc
format compact


% Create an audio input object
audioInput = audioDeviceReader('SampleRate', 48000, 'NumChannels', 1);

% Set up the figure for plotting
figure(56);
hPlot = plot(zeros(1024, 1));
title('Real-Time SPL Analysis');
xlabel('Frequency (Hz)');
ylabel('SPL (dB)');
grid on;

% Set up FFT parameters
fftSize = 2048;
spectrumSPL_old = zeros(1025, 1);

% Calibration factor (adjust this based on your microphone and setup)
calibrationFactor = 45; % For example, if your microphone reads 94 dB as 0 dB SPL

% Process audio in real-time
while ishandle(hPlot)
    audioData = audioInput();
    
    % Compute the spectrum using FFT
    spectrum = abs(fft(audioData, fftSize));
    
    % Generate frequency axis
    frequencyAxis = linspace(0, audioInput.SampleRate/2, fftSize/2 + 1);
    
    % Compute SPL value
    spectrumSPL_new = 20*log10(spectrum(1:fftSize/2 + 1)) + calibrationFactor;
    spectrumSPL = (spectrumSPL_new + spectrumSPL_old)./2;
    spectrumSPL_old = spectrumSPL_new;

    % Update the plot
    set(hPlot, 'XData', frequencyAxis, 'YData', spectrumSPL);
    xlim([100, 20000]); % Set the x-axis limit to 500 Hz to 16 kHz
    ylim([-20, 100]); % Set the y-axis limit based on your expected SPL range
    
    drawnow;
end

% Release the audio input object
release(audioInput);