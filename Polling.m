% Parameters
Fs = 48000; % Sampling frequency
bitLength = 48000; % Number of samples per bit (1 second corresponds to 48000 samples)
F0 = 4000; % Frequency of '0' bit
F1 = 8000; % Frequency of '1' bit
F_pulse = 8000; % Frequency of the pulse
stopPattern = [1,0,1]; % Stop pattern (101)

% Create audioDeviceReader object
audioReader = audioDeviceReader('SampleRate', Fs);

% Main loop
while true
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
            [~, f_index] = min(abs((0:Fs/length(fft_data):Fs/2) - F_pulse));

            % Check if the amplitude at the frequency of interest is significant
            if fft_data(f_index) > 10 * mean(fft_data) % Adjust threshold as needed
                % Pulse detected
                isPulseDetected = true;
                fprintf('Pulse detected!\n');

                % Start capturing audio data
                isCapturing = true;
                captureBuffer = audioData; % Initialize capture buffer
            end
        elseif isCapturing
            % Continue capturing audio data
            captureBuffer = [captureBuffer; audioData];
            
            % Check if capture duration has elapsed
            if length(captureBuffer) >= bitLength
                % Demodulate captured audio data
                binarySignal = demod(captureBuffer, F0, F1, Fs, bitLength);
                
                % Check if the last 3 bits match the expected stop pattern
                if isequal(binarySignal(end-2:end), stopPattern)
                    % Process the binary signal (e.g., print to console)
                    disp(binarySignal);
                    break; % Exit loop since valid signal found
                else
                    % Reset pulse detection
                    isPulseDetected = false;
                    fprintf('Stop pattern check failed! Resetting.\n');
                    break; % Exit loop since invalid signal found
                end
            end
        end
    end
end

% Release audioDeviceReader object
release(audioReader);
