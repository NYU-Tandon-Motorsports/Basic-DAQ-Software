
int previousVoltage = 128;
int thresholdVoltage = 10;
int sampleCount = 1;
double FS = 7555.2;
double k = 1/FS;
void setup() 
{
    pinMode(A1,INPUT);
    //analogReference(EXTERNAL);
    Serial.begin(9600);
    Serial.println("###Hall effect Test: IF ITS NOT WORKING, MAKE SURE THE MAGNET IS IN THE RIGHT ORIENTATION!!!");
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
         Serial.print("$$$9 Hall_Sensor 1 speed ");
         Serial.print(1/T * 60);
         Serial.print(" RPM ");
         Serial.println(millis()/1000.0);
         sampleCount = 1;
    }
    previousVoltage = voltage;   
}
