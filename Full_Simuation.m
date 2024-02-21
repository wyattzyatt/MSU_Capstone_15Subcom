clc;
clear all;
close all;

% -- Variablesfs = 48000; % Sampling frequency (samples per second)
fs = 48000;
dt = 1/fs; % seconds per sample
F1 = 4000; % Sine wave frequency (4k hertz)
F2 = 8000; % Sine wave frequency (8k hertz)


% Create an audio input object randi([0 1],1,8)
audioInput = audioDeviceReader('SampleRate', 48000, 'NumChannels', 1);
binary_string = [1 0 1 0 0 1 1 1 1 0 0 1 0 1];
%binary_string = [1 1 1 1 1 1 1 1 1 1 1 1 1 1];
%binary_string = randi([0 1],1,5);
[bfsk, t] = bfsk_signal_creation(binary_string, dt, F1, F2);
bfsk2 = [bfsk' zeros(1, fs) bfsk' zeros(1, fs) bfsk' zeros(1, fs) bfsk' zeros(1, fs) bfsk'];
soundsc(bfsk2, 48000)
figure(1)
plot(t,bfsk);
xlabel('Time (ms)');
ylabel('Amplitude');
title('BFSK Signal');
axis([-0.01 1.01 -1.1 1.1]);


demod_sig = demod(bfsk, F1, F2, fs, 14);
figure(3)
stem(1:14,demod_sig, 'LineWidth',1.5);
ylim([-0.1 1.1]);
xlabel('Time (ms)');
ylabel('Amplitude');
title('demod band signal');


function [bfsk, t] = bfsk_signal_creation(binary_string, dt, F1, F2)
    StopTime = 1; % Time duration (seconds)
    t = (0:dt:StopTime-dt)';
    binary_length = length(binary_string);
    bit_duration = StopTime / binary_length;

    % -- Binary signal creation
    binary_bit = zeros(size(t));
    for j = 1:length(t)
        % Calculate the index corresponding to the current time
        idx = floor((t(j) - t(1)) / bit_duration) + 1;
        % Ensure idx stays within the bounds of binary_string
        idx = max(min(idx, binary_length), 1);
        % Extract the binary bit from binary_string
        binary_bit(j) = binary_string(idx);
    end

    % Signal Creations
    data1 = sin(2*pi*F1*t);
    data2 = sin(2*pi*F2*t);

    % -- BFSK signal 
    BFSK = zeros(size(t));
    for j = 1:length(t)
        if binary_bit(j) == 0
            BFSK(j) = data1(j);
        else
            BFSK(j) = data2(j);
        end
    end

    figure(2)
    plot(t, binary_bit, 'LineWidth', 1.5);
    ylim([-0.1 1.1]);
    xlabel('Time (ms)');
    ylabel('Amplitude');
    title('Base band signal');
    
    bfsk = BFSK;
end

%% BFSK Demodulation Function
function demod_sig = demod(bfsk, F1, F2, fs, bitLength)

    % Compute the analytical signal (complex envelope)
    analytic_signal = hilbert(bfsk);

    % Compute the instantaneous phase of the analytic signal
    instantaneous_phase = unwrap(angle(analytic_signal));

    % Compute the instantaneous frequency (derivative of phase)
    instantaneous_frequency = diff(instantaneous_phase) / (2 * pi * (1/fs));

    % Set a threshold to decide between the two frequencies
    threshold = (F1 + F2) / 2;

    % Demodulation based on instantaneous frequency
    demod_sig = zeros(size(bfsk));
    demod_sig(instantaneous_frequency >= threshold) = 1;

    demod_sig = demod_sig(round((fs/bitLength)/2):round(fs/bitLength):end);
end