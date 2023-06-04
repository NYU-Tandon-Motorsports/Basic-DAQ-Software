double pulseWidthAdjustment = 1.0;
unsigned long tStart1 = micros();
unsigned long tStart2 = micros();
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
    double rpm = pulseWidthAdjustment * 60.0/((micros() - tStart1) / 1000000.0);
    tStart1 = micros();
    Serial.print("$$$20 Hall_Sensor 1 speed ");
    Serial.print(rpm);
    Serial.print(" RPM ");
    Serial.println(millis()/1000.0);
    sei();
}

void hall_2StopCounting()
{
    cli();
    double rpm = pulseWidthAdjustment * 60.0/((micros() - tStart2) / 1000000.0);
    tStart2 = micros();
    Serial.print("$$$21 Hall_Sensor2 1 speed ");
    Serial.print(rpm);
    Serial.print(" RPM ");
    Serial.println(millis()/1000.0);
    sei();
}

void loop() {
   
}
