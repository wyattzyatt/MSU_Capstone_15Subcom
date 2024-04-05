function demod_sig = Polling(Fs, F0, F1, captureDuration,numBitsToDemodulate)
    % Polling loop for recieving and demodulating signal 
    
    % Parameters
    % Fs = 48000; % Sampling frequency
    % F0 = 4000; 
    % F1 = 8000;
    % captureDuration = 1; % 1-second capture duration after pulse detection
    % numBitsToDemodulate = 14; % Number of bits to demodulate
    demod_sig = [];
    traverse = 0;

    % totalErrors = [];
    % 
    % knownCommand = [1 0 1 0 0 1 1 1 1 0 0 1 0 1];

    % bandpass4k = [zeros(1,round((fc4k-fr)*1024/Fs)), ones(1,round(fr*2*1024/Fs)),...
    %             zeros(1,floor((Fs-2*(fc4k+fr))*1024/Fs)), ...
    %             ones(1,round((fr*2)*1024/Fs)),zeros(1,round((fc4k-fr)*1024/Fs))];
    % bandpass8k = [zeros(1,round((fc8k-fr)*1024/Fs)), ones(1,round(fr*2*1024/Fs)),...
    %             zeros(1,floor((Fs-2*(fc8k+fr))*1024/Fs)), ...
    %             ones(1,round((fr*2)*1024/Fs)),zeros(1,round((fc8k-fr)*1024/Fs))];
    % %bandpass8k = [zeros(1,(fc8k-fr)), ones(1,fr*2), zeros(1,(Fs-2*(fc8k+fr))), ones(1,(fr*2)),zeros(1,(fc8k-fr))];
    % bandpassFilter = bandpass8k | bandpass4k;
    % figure();
    % plot(bandpassFilter);

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
            % Create bandpass filter coefficients for 4000 Hz and 8000 Hz
            [b, a] = butter(4, [3900 8100]/(Fs/2), 'bandpass');
            
            % Apply bandpass filter to the incoming signal
            audioData = filter(b, a, audioData);
    
            % Check for pulse
            if ~isPulseDetected
                % Perform FFT on the audio data
                fft_data = abs(fft(audioData));
                % freqs = linspace(0,Fs,length(audioData));
                % figure(69);
                % plot(freqs,fft_data);
            
                % fft_data = fft_data.*bandpassFilter';
                % figure(73);
                % plot(freqs,fft_data);
                % ylim([0, 100])
                % Find the index corresponding to the frequency of interest (8 kHz)
                [~, f_index] = min(abs((0:Fs/length(fft_data):Fs/2) - 8000));
    
                % Check if the amplitude at the frequency of interest is significant
                if fft_data(f_index) > 17 * mean(fft_data) & mean(fft_data)>0.003 % Adjust threshold as needed
                    % Pulse detected
                    isPulseDetected = true;
                    fprintf('Pulse detected!\n');
    
                    % Start capturing audio data
                    isCapturing = true;
                    captureBuffer = audioData; % Initialize capture buffer
                    
                    captureBuffer = sgolayfilt(captureBuffer,13,15); %Pool Parameters (13, 15)
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
                    %figure;
                    t = (0:length(captureBuffer)-1) / Fs; % Time vector
                    % plot(t, captureBuffer);
                    % xlabel('Time (s)');
                    % ylabel('Amplitude');
                    % close(figure);
                    demod_sig = demod(captureBuffer, F0, F1, Fs, numBitsToDemodulate, captureDuration);
                    

                    % Save the demodulated signal plot as a figure
                    % fig = figure('visible', 'off');
                    % stem(1:numBitsToDemodulate, demod_sig(1:numBitsToDemodulate), 'LineWidth', 1.5);
                    % ylim([-0.1 1.1]);
                    % xlabel('Time (ms)');
                    % ylabel('Amplitude');
                    % title('Demodulated Signal');
                    % % Generate filename with timestamp
                    % demodFilename = fullfile('Figures', ['demodulated_signal_', datetime('now'), '.png']);
                    % saveas(fig, demodFilename);
                    % close(fig); % Close the figure

                    disp(demod_sig');
                    % Compare received bits with known command
                    % num_errors = sum(abs(demod_sig(1:14)' - knownCommand));
                    % totalErrors = [totalErrors, num_errors];
                    release(audioReader);
                    break; % Exit loop since valid signal found
                    
                end
            end
        end
    end
    % Release audioDeviceReader object
    %[S,F,T] = spectrogram(captureBuffer,round(Fs*.02),[],[],Fs); figure(); imagesc(T,F,log(abs(S))); set(gca,'YDir','Normal');
    release(audioReader);
end