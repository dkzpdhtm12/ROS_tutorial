//#include <ros.h>
//#include <std_msgs/String.h>
#include <AFMotor.h>
#include <string.h>

AF_DCMotor motor_R(2);
AF_DCMotor motor_L(4);
ros::NodeHandle nh;

void fr(const std_msgs::String& cmd_msg)
{
    command = cmd_msg.data;
    if (command == "z"){

      motor_R.run(BACKWARD);
      motor_L.run(FORWARD);
    }

    else if (command == "x")
    {
      motor_R.run(BACKWARD);
      motor_L.run(BACKWARD);
    }

    else if (command == "y")
    {
      motor_R.run(FORWARD);
      motor_L.run(FORWARD);
    }

    else if (command == "w")
    {
      motor_R.run(RELEASE);
      motor_L.run(RELEASE);
    }
}

ros::Subscriber<std_msgs::String> sub("/front", fr);

void setup()
{
    Serial.begin(9600);

    motor_R.setSpeed(230);
    motor_L.setSpeed(230);
 
    motor_R.run(RELEASE);
    motor_L.run(RELEASE);

    nh.initNode();
    nh.subscribe(sub);
}

void loop()
{
    nh.subscribe(sub);
    nh.spinOnce();
}
