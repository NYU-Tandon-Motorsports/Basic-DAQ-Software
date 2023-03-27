#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
//#include <SD.h>
#include "SdFat.h"
SdFat SD;

#define SD_CS_PIN SS

File myFile;



/* This driver reads raw data from the BNO055

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3V DC
   Connect GROUND to common ground

   History
   =======
   2015/MAR/03  - First release (KTOWN)
*/

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28);

/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(57600);
  Serial.println("###Orientation Sensor Raw Data Test"); Serial.println("");

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("!!!Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  /* Display the current temperature */
  int8_t temp = bno.getTemp();
  Serial.print("###Current Temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  Serial.println("");

  bno.setExtCrystalUse(true);

  Serial.print("###Initializing SD card...");
if (!SD.begin(SD_CS_PIN)) {
Serial.println("!!!initialization failed!");
return;
}

  Serial.println("Calibration status values: 0=uncalibrated, 3=fully calibrated");
  SD.remove("test.txt");
  //myFile=SD.open("test.txt",FILE_WRITE);
  //myfile.print("Hello");
  //myfile.close();
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
  // Possible vector values can be:
  // - VECTOR_ACCELEROMETER - m/s^2
  // - VECTOR_MAGNETOMETER  - uT
  // - VECTOR_GYROSCOPE     - rad/s
  // - VECTOR_EULER         - degrees
  // - VECTOR_LINEARACCEL   - m/s^2
  // - VECTOR_GRAVITY       - m/s^2
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
  //myFile=SD.open("test.txt",FILE_WRITE);
  //myFile.seek(EOF);
  // Display the floating point data
  Serial.print("$$$0 ");
  Serial.print("DOF9 ");
  Serial.print("3 ");
  Serial.print("x,y,z ");
  Serial.print(euler.x(), 3);
  Serial.print(",");
  Serial.print(euler.y(), 3);
  Serial.print(",");
  Serial.print(euler.z(), 3);
  Serial.print(" ");
  Serial.print("m/s2,m/s2,m/s2 ");
  Serial.println(millis()/1000.0, 3);
  delay(50);
  /*
  // Quaternion data
  imu::Quaternion quat = bno.getQuat();
  Serial.print("qW: ");
  Serial.print(quat.w(), 4);
  Serial.print(" qX: ");
  Serial.print(quat.x(), 4);
  Serial.print(" qY: ");
  Serial.print(quat.y(), 4);
  Serial.print(" qZ: ");
  Serial.print(quat.z(), 4);
  Serial.print("\t\t");
  */

  /* Display calibration status for each sensor.
  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);
  Serial.print("CALIBRATION: Sys=");
  Serial.print(system, DEC);
  Serial.print(" Gyro=");
  Serial.print(gyro, DEC);
  Serial.print(" Accel=");
  Serial.print(accel, DEC);
  Serial.print(" Mag=");
  Serial.println(mag, DEC);
*/
  /*float time=millis()/1000;
  if (myFile){
    myFile.print(time);
    myFile.print("\t");
    myFile.print("X: ");
    myFile.print(euler.x());
    myFile.print(" Y: ");
    myFile.print(euler.y());
    myFile.print(" Z: ");
    myFile.print(euler.z());
    myFile.print("\n");
    myFile.close();
  */


}
