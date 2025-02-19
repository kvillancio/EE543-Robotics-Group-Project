

% Set the ROS domain variable to 88
setenv('ROS_DOMAIN_ID', '88');

% create ros2 node
PubSubTestNode = ros2node("PubSubTestNode");

% create publisher for test data
Pub = ros2publisher(PubSubTestNode, "/ExampleTopic", "std_msgs/Int32MultiArray");

% create subscriber for test data
Sub = ros2subscriber(PubSubTestNode, "/ExampleTopic", "std_msgs/Int32MultiArray", @PubSubExampleCallback);


% initialize empty message
msg = ros2message("std_msgs/Int32MultiArray");
% fill message with random integers between 1 and 100
msg.data = int32(randi([1,100]));

% infinite loop:
while(true)
    if ~exist("loopcount", "var")
        loopCount = 0;
    end
        
    loopCount = loopCount + 1;

    msg.data(1) = int32(randi([1,100]));
    msg.data(2) = int32(loopCount);

    send(Pub, msg);

    pause(1);
end


% callback for whenever the subscriber sees a newly published message
function PubSubExampleCallback(message)
fprintf("test data: #%3.d, (%d number of messages:)\n", message.data(1), message.data(2));
end