% Polling loop for recieving and demodulating signal 
function demod_sig = Polling(Fs, F0, F1, captureDuration,numBitsToDemodulate)
    % Parameters
    Fs = 48000; % Sampling frequency
    F0 = 4000; 
    F1 = 8000;
    captureDuration = 1; % 1-second capture duration after pulse detection
    numBitsToDemodulate = 14; % Number of bits to demodulate
    demod_sig = [];

    % Create audioDeviceReader object
    audioReader = audioDeviceReader('SampleRate', Fs);
    % Main loop
    while isempty(demod_sig)
        % Reset flags and buffers
        isPulseDetected = false;
        isCapturing = false;
        captureBuffer = [];
    
        % Read audio data until a valid signal is found
        while true
            % Read a chunk of audio data
            audioData = audioReader();
    
            % Check for pulse
            if ~isPulseDetected
                % Perform FFT on the audio data
                fft_data = abs(fft(audioData));
    
                % Find the index corresponding to the frequency of interest (8 kHz)
                [~, f_index] = min(abs((0:Fs/length(fft_data):Fs/2) - 8000));
    
                % Check if the amplitude at the frequency of interest is significant
                if fft_data(f_index) > 4 * mean(fft_data) % Adjust threshold as needed
                    % Pulse detected
                    isPulseDetected = true;
                    fprintf('Pulse detected!\n');
    
                    % Start capturing audio data
                    isCapturing = true;
                    captureBuffer = audioData; % Initialize capture buffer
    
                    % Start measuring time
                    startTime = tic;
                end
            elseif isCapturing
                % Continue capturing audio data
                captureBuffer = [captureBuffer; audioData];
    
                % Check if capture duration has elapsed
                elapsedTime = toc(startTime);
                if elapsedTime >= captureDuration
                    % Plot the capture buffer (for visualization)
                    figure;
                    t = (0:length(captureBuffer)-1) / Fs; % Time vector
                    plot(t, captureBuffer);
                    xlabel('Time (s)');
                    ylabel('Amplitude');
                    title('Captured Signal');
    
                    % Demodulate captured audio data
                    demod_sig = demod(captureBuffer, F0, F1, Fs, numBitsToDemodulate);
    
                    % Process the binary signal (e.g., print to console)
                    disp(demod_sig);
                    break; % Exit loop since valid signal found
                end
            end
        end
    end
    % Release audioDeviceReader object
    %[S,F,T] = spectrogram(captureBuffer,round(Fs*.02),[],[],Fs); figure(); imagesc(T,F,log(abs(S))); set(gca,'YDir','Normal');
    release(audioReader);
end