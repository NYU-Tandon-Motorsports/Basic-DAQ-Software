double pulseWidthAdjustment = 1.0;
double tStart1 = millis();
double tStart2 = millis();
void setup()
{
    pinMode(2,INPUT_PULLUP);
    pinMode(3,INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(2),hall_1StopCounting,FALLING);
    attachInterrupt(digitalPinToInterrupt(3),hall_2StopCounting,FALLING);
    Serial.begin(115200);
    Serial.println("###Hall effect Test: IF ITS NOT WORKING, MAKE SURE THE MAGNET IS IN THE RIGHT ORIENTATION!!!");
}

void hall_1StopCounting()  //Falling edge
{
    cli();
    double rpm = pulseWidthAdjustment * 60/((millis() - tStart1) / 1000);
    tStart1 = millis();
    Serial.print("$$$20 Hall_Sensor 1 speed ");
    Serial.print(rpm);
    Serial.print(" RPM ");
    Serial.println(millis()/1000.0);
    sei();
}

void hall_2StopCounting()
{
    cli();
    double rpm = pulseWidthAdjustment * 60/((millis() - tStart2) / 1000);
    tStart2 = millis();
    Serial.print("$$$21 Hall_Sensor2 1 speed ");
    Serial.print(rpm);
    Serial.print(" RPM ");
    Serial.println(millis()/1000.0);
    sei();
}

void loop() {
   
}
