from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase

class Neural_Distance:
    def __init__(self, distancia):
        # Initialize the EV3 Brick.
        self.ev3 = EV3Brick()
        self.sensorUlt = UltrasonicSensor(Port.S4)

        # The DriveBase is composed of two motors, with a wheel on each motor.
        # The wheel_diameter and axle_track values are used to make the motors
        # move at the correct speed when you give a motor command.
        # The axle track is the distance between the points where the wheels
        # touch the ground.

        self.motorDir = Motor(Port.B)
        self.motorEsq = Motor(Port.C)
        self.robot = DriveBase(self.motorEsq, self.motorDir, wheel_diameter=55.5, axle_track=104) 

        #Parâmetros da rede
        self.dist = distancia
        self.bias = -0.39651959669023307 # -0.4
        self.pesoSensor = 0.9995105730045505 # 1
        self.pesoDist = -0.9855879007070074 # -0.99

    def calcular_velocidade(self):
        distancia = self.sensorUlt.distance() / 10
        velocidade = self.bias + (distancia * self.pesoSensor) + (self.dist * self.pesoDist)
        return velocidade
        
    def executar(self):
        while True:
            velocidade = self.calcular_velocidade()
            self.robot.drive(velocidade, 0)

controlador = Neural_Distance(30)
controlador.executar()


    