#include <Stepper.h>

//  Define serial input flags
const int CW_X_FLAG = 1;  // Send a character '1' over serial to move horizontal-axis motor clockwise
const int CCW_X_FLAG = 2; // Send a character '2' over serial to move horizontal-axis motor counterclockwise
const int CW_Y_FLAG = 3;  // Send a character '3' over serial to move vertical-axis motor clockwise
const int CCW_Y_FLAG = 4; // Send a character '4' over serial to move vertical-axis motor counterclockwise

//  Define stepper motor pins
//    Horizontal plane motor
const int STEPPER_HP_1 = 30;
const int STEPPER_HP_2 = 31;
const int STEPPER_HP_3 = 32;
const int STEPPER_HP_4 = 33;
//    Vertical plane motor
const int STEPPER_VP_1 = 36;
const int STEPPER_VP_2 = 37;
const int STEPPER_VP_3 = 38;
const int STEPPER_VP_4 = 39;

//  Define stepper motor parameters
const int STEPPER_STEPS_PER_REV = 200; //  steps per revolution
const int NUM_STEPS_PER_REQ = 1;
const int STEPPER_SPEED = 35;

//  Initialize the stepper motors
//      CW = forward = positive step, CCW = backward = negative step
//    Horizontal plane
Stepper stepper_motor_hp(STEPPER_STEPS_PER_REV, STEPPER_HP_1, STEPPER_HP_2, STEPPER_HP_3, STEPPER_HP_4);
//    Vertical plane
Stepper stepper_motor_vp(STEPPER_STEPS_PER_REV, STEPPER_VP_1, STEPPER_VP_2, STEPPER_VP_3, STEPPER_VP_4);

//  Initialize some working variables
char in_byte = ' ';
int in_num;

/*
 * Expecting an ASCII character of an integer ('0' --> '9') as serial input, 
 * returns that ASCII integer as an int.
 */
int get_serial_input_as_int() {
  in_byte = Serial.read();

  return int(in_byte - '0');  //  Input is ASCII character of a single digit integer. Convert to int.
}


void setup() {
  Serial.begin(9600);

  stepper_motor_hp.setSpeed(STEPPER_SPEED);
  stepper_motor_vp.setSpeed(STEPPER_SPEED);
}

void loop() {
  if(Serial.available()) {
    in_num = get_serial_input_as_int();
    
    if(in_num == CCW_X_FLAG) { stepper_motor_hp.step(-NUM_STEPS_PER_REQ); }
    else if (in_num == CW_X_FLAG) { stepper_motor_hp.step(NUM_STEPS_PER_REQ); }
    else if (in_num == CCW_Y_FLAG) { stepper_motor_vp.step(-NUM_STEPS_PER_REQ); }
    else if (in_num == CW_Y_FLAG) { stepper_motor_vp.step(NUM_STEPS_PER_REQ); }
  }  
}
