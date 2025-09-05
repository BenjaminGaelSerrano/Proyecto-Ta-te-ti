

// Pines del HC-SR04
const int trigPin = 11;
const int echoPin = 10;

void setup() {
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  
    // Si detecta movimiento, medir distancia
    long duration;
    float distance;

    // Enviar pulso ultrasónico
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Leer tiempo de eco
    duration = pulseIn(echoPin, HIGH);

    // Convertir a cm
    distance = duration * 0.034 / 2;

    // Verificar si está a menos de 1 metro (100 cm)
    if (distance <= 50) {
      Serial.println("x");
      delay(3000);
    }

  

  delay(10);
}
