void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming string
    String intStr = Serial.readStringUntil('\n');
    
    // Convert the string to an integer
    int intData = intStr.toInt();
    
    // Print the received integer data to the serial monitor
    Serial.print("Received integer data: ");
    Serial.println(intData);
  }
}
