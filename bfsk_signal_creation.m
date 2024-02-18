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