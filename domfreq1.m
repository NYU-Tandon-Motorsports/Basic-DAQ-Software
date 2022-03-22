Fs = 100; % sampling frequency 1 kHz
x = [0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0]; % time series
t = [1:1:max(size(x))]; % time scale
x = x - mean(x);                                            % <= ADDED LINE
plot(t,x), axis('tight'), grid('on'), title('Time series'), figure
nfft = 512; % next larger power of 2
y = fft(x,nfft); % Fast Fourier Transform
y = abs(y.^2); % raw power spectrum density
y = y(1:1+nfft/2); % half-spectrum
[v,k] = max(y); % find maximum
f_scale = (0:nfft/2)* Fs/nfft; % frequency scale
plot(f_scale, y),axis('tight'),grid('on'),title('Dominant Frequency')
fest = f_scale(k); % dominant frequency estimate
fprintf('Dominant freq.: true %f Hz, estimated %f Hznn\n', fest, fest)
fprintf('Frequency step (resolution) = %f Hznn\n', f_scale(2))
