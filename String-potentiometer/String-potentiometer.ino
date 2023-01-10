void setup() 
{
    Serial.begin(9600);
    Serial.println("###String Potentiometer Test");
}

void loop() {
    
    int voltage = analogRead(A3);
    //(max_distance/max_analogRead) * (analogRead - minAnalogRead)
    double distance = (66.75/1006)*(voltage - 8.0);
    Serial.print("$$$18 StringPot 1 stringdistance ");
    Serial.print(distance);
    Serial.print(" cm ");
    Serial.println(millis()/1000.0);
    delay(100);
}
