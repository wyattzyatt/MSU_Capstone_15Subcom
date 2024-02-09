%% BFSK Creation Function
function [bfsk, t] = Subcom15_BFSK(binary_string, dt, F1, F2)
    
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
    soundsc(bfsk, 1/dt);
end