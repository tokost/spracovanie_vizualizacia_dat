from car import Car

clas Car:   # 1.
    
    make = None   # 2.
    model = None
    year = None
    color = None

    def drive(self):                  # 3.
        print("This car is driving")

    def stop(self):
        print("This car is stopped")