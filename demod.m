%% BFSK Demodulation Function
function demod_sig = demod(bfsk, F1, F2, fs, bitLength)

    % Compute the analytical signal (complex envelope)
    analytic_signal = hilbert(bfsk);

    % Compute the instantaneous phase of the analytic signal
    instantaneous_phase = unwrap(angle(analytic_signal));

    % Compute the instantaneous frequency (derivative of phase)
    instantaneous_frequency = diff(instantaneous_phase) / (2 * pi * (1/fs));

    % Set a threshold to decide between the two frequencies
    threshold = ((F1-500) + (F2-500)) / 2;

    % Demodulation based on instantaneous frequency
    demod_sig = zeros(size(bfsk));
    demod_sig(instantaneous_frequency >= threshold) = 1;
    disp(bitLength);
    demod_sig = demod_sig(round((fs/bitLength)/2):round(fs/bitLength):end-round((fs/bitLength)/2));
end