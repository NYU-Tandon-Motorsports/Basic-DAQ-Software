
int previousVoltage = 128;
int thresholdVoltage = 10;
int sampleCount = 1;
double FS = 7561.47;
double k = 1/FS;
double deltaThreshold = 500; //200 rpm/sample
double previousValue = -1;
double tStart = 0;
void setup() 
{
    pinMode(A1,INPUT);
    //analogReference(EXTERNAL);
    Serial.begin(9600);
    Serial.println("###Hall effect Test: IF ITS NOT WORKING, MAKE SURE THE MAGNET IS IN THE RIGHT ORIENTATION!!!");
    tStart = millis()/1000.0;
}


void loop() {
    //Serial.print("$$$1 SteeringAngle 1 voltage ");
    //Serial.print(voltage);
    int voltage = analogRead(A1);
    if (voltage > thresholdVoltage && previousVoltage > thresholdVoltage)
    {
        sampleCount++;
    }
    else if (voltage < thresholdVoltage && previousVoltage > thresholdVoltage)
    {
         int n = sampleCount;
         double T = n * k;
         double rpm = 1/T * 60;
         if (previousValue == -1)
         {
              if (millis()/1000 - tStart < 5)
              {
                   rpm = 0;
                   previousValue = -1;
              }
              else
              {
                  previousValue = rpm;
              }
         }
         else
         {
              if (abs(rpm - previousValue) > deltaThreshold)
              {
                  rpm = previousValue;
              }
              else
              {
                  previousValue = rpm;
              }
         }
         if (rpm < 200)
         {
              deltaThreshold = 2000;
         }
         else if (rpm > 200 && rpm < 800)
         {
              deltaThreshold = 500;
         }
         else
         {
              deltaThreshold = 200;
         }
         Serial.print("$$$9 Hall_Sensor 1 speed ");
         Serial.print(rpm);
         Serial.print(" RPM ");
         Serial.println(millis()/1000.0);
         sampleCount = 1;
    }
    previousVoltage = voltage;   
}
