clc;
clear all;
close all;

% -- Variables
fs = 48000; % Sampling frequency (samples per second)
dt = 1/fs; % seconds per sample
F1 = 4000; % Sine wave frequency (4k hertz)
F2 = 8000; % Sine wave frequency (8k hertz)

binary_string = randi([0 1],1,8);
[bfsk, t] = bfsk_signal_creation(binary_string, dt, F1, F2);
figure(1)
plot(t,bfsk);
xlabel('Time (ms)');
ylabel('Amplitude');
title('BFSK Signal');
axis([-0.01 1.01 -1.1 1.1]);


demod_sig = [];
demod_sig = demod(bfsk, F1, F2, fs);
figure(3)
plot(t,demod_sig, 'LineWidth',1.5);
ylim([-0.1 1.1]);
xlabel('Time (ms)');
ylabel('Amplitude');
title('demod band signal');




%% BFSK Creation Function
function [bfsk, t] = bfsk_signal_creation(binary_string, dt, F1, F2)
    
    StopTime = 1; % Time duration (seconds)
    t = (0:dt:StopTime-dt)';
    i=1/8;

    % -- Binary signal creation
    for j=1:length(t)
        if t(j)<=i
            binary_bit(j)=binary_string(i*8);
        else
            binary_bit(j)=binary_string(i*8);
            i=i+1/8;
        end
    end

    % Signal Creations
    data1 = sin(2*pi*F1*t);
    data2 = sin(2*pi*F2*t);

    % -- BFSK signal 
    for j = 1:length(t)
        if binary_bit(j) == 0
            BFSK(j)=data1(j);
        else
            BFSK(j)=data2(j);
        end
    end

    figure(2)
    plot(t,binary_bit, 'LineWidth',1.5);
    ylim([-0.1 1.1]);
    xlabel('Time (ms)');
    ylabel('Amplitude');
    title('Base band signal');
    
    bfsk = BFSK;
end

%% Demodulation Function 
% The hilbert function in MATLAB returns the analytic signal, also known as
% the complex envelope, of a real-valued signal. The complex envelope is a 
% complex signal that captures the amplitude and phase information of the 
% original real-valued signal. The hilbert function is commonly used in 
% signal processing for tasks such as envelope detection and phase analysis.
%
% "analytic_signal" is the complex envelope obtained using the Hilbert 
% transform.
%
% "angle(analytic_signal)" calculates the phase angle of the complex
% numbers in analytic_signal. The angle function returns values in the 
% range [-π, π].
%
% "unwrap" is used to unwrap the phase angle to avoid abrupt jumps between
% -π and π. This ensures a smooth representation of the phase over time.
%
% "diff" calculates the discrete difference of the elements in
% instantaneous_phase, representing the change in phase over time.
%
% Dividing by (2 pi * (1 / fs)) scales the phase difference to obtain the 
% instantaneous frequency in Hertz

function demod_sig = demod(bfsk, F1, F2, fs)
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
end