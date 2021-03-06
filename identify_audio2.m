Files=dir('*.wav*');
full_data = [];

names = strings(size(full_data,2));

for k=1:length(Files)
   FileName=Files(k).name;
   names(k) = FileName(1:end-5);
   [data, f] = audioread(FileName);
   data = [data;  zeros((200000-length(data)),1)];
   full_data(:,k) = data;
end

train_vec = zeros(200000,size(full_data,2));
test_vec = zeros(200000,size(full_data,2));

training_answers = strings(size(full_data,2));
test_answers = strings(size(full_data,2));

for k=1:4:size(full_data,2)
    test_vec(:,k) = full_data(:,k);
    test_answers(k) = names(k);

    train_vec(:,k+1) = full_data(:,k+1);
    training_answers(k+1) = names(k+1);
    train_vec(:,k+2) = full_data(:,k+2);
    training_answers(k+2) = names(k+2);
    train_vec(:,k+3) = full_data(:,k+3);
    training_answers(k+3) = names(k+3);
end

test_vec = test_vec(:,(any(test_vec,1)));
train_vec = train_vec(:,(any(train_vec,1)));

test_answers(cellfun('isempty',test_answers)) = [];
training_answers(cellfun('isempty',training_answers)) = [];


train_vec_ms=(train_vec-mean(train_vec,2))./vecnorm(train_vec-mean(train_vec,2));

% subtract the mean and normalize the test images
test_vec_ms=(test_vec-mean(test_vec,2))./vecnorm(test_vec-mean(test_vec,2));

% train_vec_ms = train_vec;
% test_vec_ms = test_vec;

train_vec_ms = train_vec_ms(:,1:48);
test_vec_ms = test_vec_ms(:,1:16);












[U,~,~] = svd(train_vec_ms, 'econ');

% Choose the desired eigenfaces, excluding the first one
% U = U(:, 2:number);

sound(U(:,8),48000)

% Multiply by U to decompose test_vec_ms and train_vec_ms into linear
% combination of U vectors
x = U'*(test_vec_ms);

z = U'*(train_vec_ms);


% Run guessing algorithm by finding the image in training that is most
% similar to the test image and returning the guessed index
guesses = zeros(size(test_vec_ms,2));
for im=1:size(test_vec_ms,2)
    exampleImage = x(:,im);
%     err = sum(abs(exampleImage-z));
%     err = sqrt(sum((exampleImage-z).^2));
    err = vecnorm(exampleImage-z);
    [~,index] = min(abs(err));
    guesses(im) = index;
end

% Remove unwanted zeros
guesses = guesses(:,1);









correct = zeros(size(test_vec_ms,2));
for i=1:size(test_vec_ms,2)
    named_guess(i) = training_answers(guesses(i));
    if test_answers(i) == named_guess(i)
        correct(i) = 1;
    else
        correct(i) = 0;
        
    end
    
    
end

correct = correct(:,1);

% Final Percentage
resultant = sum(correct)/length(correct)
