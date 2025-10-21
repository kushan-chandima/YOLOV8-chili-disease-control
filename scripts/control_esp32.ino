#include <Stepper.h>

// Define stepper motor connections
#define IN1 13  // D13
#define IN2 12  // D12
#define IN3 14  // D14
#define IN4 27  // D27

// Define LED and Rain Sensor
#define Pump 2   // LED connected to D34
#define RAIN_SENSOR_PIN 35  // Rain sensor connected to D35

// Steps per revolution for 28BYJ-48 (gear reduction 64:1, motor step 2048)
#define STEPS_PER_REV 2048

// Create stepper motor instance
Stepper stepperMotor(STEPS_PER_REV, IN1, IN3, IN2, IN4); // Proper sequence

int currentPosition = 0;  // Stores current step position
bool PumpState = false;       // Tracks LED status

void setup() {
  Serial.begin(115200); // Initialize Serial Monitor
  stepperMotor.setSpeed(10); // Set stepper motor speed (RPM)

  pinMode(Pump, OUTPUT);
  pinMode(RAIN_SENSOR_PIN, INPUT);
  //pinMode(RAIN_SENSOR_PIN2, INPUT);
  //pinMode(RAIN_SENSOR_PIN3, INPUT);
  //pinMode(RAIN_SENSOR_PIN4, INPUT);
  //digitalWrite(Pump, LOW); // LED off initially
}

void moveToPosition(int targetSteps) {
  int moveSteps = targetSteps - currentPosition;
  stepperMotor.step(moveSteps);
  currentPosition = targetSteps; // Update position
  Serial.print("Moved to ");
  Serial.print(currentPosition * 360.0 / STEPS_PER_REV);
  Serial.println(" degrees.");
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    switch (command) {
      case '0': // Reset to default (home) position
      PumpState = false;
      digitalWrite(Pump, LOW); // Turn off LED when reset
      delay(1000),
        Serial.println("Returning to default position...");
        stepperMotor.step(-currentPosition); // Move back to zero
        currentPosition = 0;
        
        Serial.println("Default position set.");
        return;

      case '1': moveToPosition((90 * STEPS_PER_REV) / 360);
        digitalWrite(Pump, HIGH); // Turn on LED after completing all movements
        PumpState = true;
        Serial.println("All angles completed, LED ON.");
        break;
      case '2': moveToPosition((-90 * STEPS_PER_REV) / 360);
        digitalWrite(Pump, HIGH); // Turn on LED after completing all movements
        PumpState = true;
        Serial.println("All angles completed, LED ON.");
        break;
      case '3': moveToPosition((135 * STEPS_PER_REV) / 360);
        digitalWrite(Pump, HIGH); // Turn on LED after completing all movements
        PumpState = true;
        Serial.println("All angles completed, LED ON.");
        break;
      case '4':
        moveToPosition((-135 * STEPS_PER_REV) / 360);
        digitalWrite(Pump, HIGH); // Turn on LED after completing all movements
        PumpState = true;
        Serial.println("All angles completed, LED ON.");
        break;

      default:
        Serial.println("Invalid input! Enter 0, 1, 2, 3, or 4.");
        return;
    }
  }

  // Check for rain after LED is on
  if (PumpState && digitalRead(RAIN_SENSOR_PIN) == LOW) { // Rain detected (LOW means rain detected)
    PumpState = false;
    digitalWrite(Pump, LOW); // Turn off LED
    delay(1000),
    Serial.println("Rain detected! Returning to default position...");
    stepperMotor.step(-currentPosition); // Move back to zero
    currentPosition = 0;
    
    Serial.println("Default position set.");
  }
}
