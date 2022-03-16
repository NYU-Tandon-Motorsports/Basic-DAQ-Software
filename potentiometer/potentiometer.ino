void setup() 
{
    pinMode(A0,INPUT);
    pinMode(A2,INPUT);
    analogReference(EXTERNAL);
    Serial.begin(9600);
    Serial.println("###Potentiometer + Hall effect Test");
}

void loop() {
    double voltage = analogRead(A0);
    //Serial.print("$$$1 SteeringAngle 1 voltage ");
    //Serial.print(voltage);
    //Serial.print(" V ");
    //Serial.println(millis()/1000.0);
    Serial.println(analogRead(A2));
    Serial.println(digitalRead(A2));
    delay(100);
}
