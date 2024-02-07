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

function demod_sig = Subcom15_Demodulate(bfsk, F1, F2, fs)
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

    demod_sig = demod_sig(3000:6000:end);
end