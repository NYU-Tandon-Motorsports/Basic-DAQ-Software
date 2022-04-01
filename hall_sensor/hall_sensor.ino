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

    int voltage[100];
    for(int i = 0; i<100; i++){
          voltage[i] = analogRead(A1);
          delay(1);
    }
    Serial.print("$$$2 Hall_Signal 100 voltage ");
    for (int i = 0; i<100; i++)
    {
        Serial.print(voltage[i]);
        if (i != 99)
        {
          Serial.print(",");
        }
    }
    Serial.print(" V ");
    Serial.println(millis()/1000.0);
}
