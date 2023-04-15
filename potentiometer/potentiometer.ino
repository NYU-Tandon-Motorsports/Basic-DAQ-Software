void setup() 
{
    Serial.begin(9600);
    Serial.println("###Potentiometer Test");
}

void loop() {
    
    int voltage = analogRead(A0)*(35.0/1023.0);
    Serial.print("$$$1 SteeringAngle 1 voltage ");
    Serial.print(voltage);
    Serial.print(" V ");
    Serial.println(millis()/1000.0, 4);
    delay(100);
}
