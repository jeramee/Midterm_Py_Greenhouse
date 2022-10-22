from pprint import pprint
from datetime import datetime
from greenhouse import Greenhouse
from greenhouse.models import Job, Command, Measure
from greenhouse.utils import get_serial_port, get_serial_connection



'''database to keep track of the greenhouse plants'''
def createGreenhouseDB():
    db = sqlite3.connect('greenhouse.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Devices(Device TEXT, State TEXT, Counter INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Measures(Type TEXT, Value TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Commands(Equipment TEXT, Command TEXT, Mode TEXT)''')
    db.commit() # Save (commit) the changes
    for row in rows:
        if row[0] == 'Infrared lamp':
           ComLamp = row[1]
           ModeLamp = row[3]
        if row[0] == 'Pump':
           ComPump = row[1]
           ModePump = row[3]
        if row[0] == 'Servomotor':
            ComServo = row[1]
            ModeServo = row[3]
        if row[0] == 'Proceed':
            ComProceed = row[1]
            ModeProceed = row[3]
        if row[0] == 'Fan':
            ComTwenty = row[1]
            ModeTwenty = row[3]
    ClosingDB(db)
    return (ComLamp,ComPump,ComServo,ComProceed,ComTwenty,ModeLamp,ModePump,ModeServo,ModeProceed,ModeTwenty)


'''Detection change of state of an equipment'''
def DetectData(ComLamp,ComPump,ComServo,ComProceed,ComTwenty,ModeLamp,ModePump,ModeServo,ModeProceed,ModeTwenty):
    ComLampPrec,ComPumpPrec,ComServoPrec,ComProceedPrec,ComTwentyPrec,ModeLampPrec,ModePumpPrec,ModeServoPrec,ModeProceedPrec,ModeTwentyPrec = Analysis()
    if ComLamp != ComLampPrec:
        if ComLamp == 'ON':
            DevCounter(ComLamp,'Infrared_lamp')
        ser.write(ComLamp)
        print 'Change of state of the infrared lamp'
    if ComPump != ComPumpPrec:
        if ComPump == 'ON':
            DevCounter(ComPump,'Pump')
        ser.write(ComPump)
        print 'Change of state of the pump'
    if ComServo != ComServoPrec:
        if ComServo == 'ON':
            DevCounter(ComServo,'Servomotor')
        ser.write(ComServo)
        print 'Change of state of the servo'
    if ComProceed != ComProceedPrec:
        if ComProceed == 'ON':
            DevCounter(ComProceed,'Valve')
        ser.write(ComProceed)
        print 'Change of state of the valve'
    if ComTwenty != ComTwentyPrec:
        if ComTwenty == 'ON':
            DevCounter(ComTwenty,'Fan')
        ser.write(ComTwenty)
        print 'Change of state of the fan'
    if ModeLamp != ModeLampPrec:
        ser.write(ModeLamp)
        print 'Change of mode of the infrared lamp'
    if ModePump != ModePumpPrec:
        ser.write(ModePump)
        print 'Change of mode of the pump'
    if ModeServo != ModeServoPrec:
        ser.write(ModeServo)
        print 'Change of mode of the servo'
    if ModeProceed != ModeProceedPrec:
        ser.write(ModeProceed)
        print 'Change of mode of the valve'
    if ModeTwenty != ModeTwentyPrec:
        ser.write(ModeTwenty)
        print 'Change of mode of the fan'
    return ComLamp,ComPump,ComServo,ComProceed,ComTwenty,ModeLamp,ModePump,ModeServo,ModeProceed,ModeTwenty

'''Function to count the number of times an equipment is used'''
def DevCounter(Com,Dev):
    db = sqlite3.connect('greenhouse.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Devices WHERE Device = ?",(Dev,))
    row = cursor.fetchone()
    if row[1] == 'ON':
        cursor.execute("UPDATE Devices SET Counter = ? WHERE Device = ?",(row[2]+1,Dev))
        db.commit()
    ClosingDB(db)       

'''Function to close the database'''
def ClosingDB(db):
    db.close()
    
'''Function to send the data to the server'''
def SendData():
    db = sqlite3.connect('greenhouse.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Data")
    rows = cursor.fetchall()
    for row in rows:
        if row[0] == 'Temperature':
            temp = row[1]
        if row[0] == 'Humidity':
            hum = row[1]
        if row[0] == 'Light':
            light = row[1]
        if row[0] == 'Moisture':
            moist = row[1]
    ClosingDB(db)
    data = {'Temperature':temp,'Humidity':hum,'Light':light,'Moisture':moist}
    r = requests.post('https://github.com/jeramee/Midterm_Py_Greenhouse.git
    print r.text

'''Add 50 vegetable:lettucce Plants'''
'''Add 25 vegetable:carrots Plants'''
'''Add 25 fruit:tomatoes Plants'''
'''Add 6 fruit:peppers Plants'''
'''Function to create list of Tuples for predefined plants'''
def FillInventory():
    inventory = [('lettuce',50),('carrots',25),('tomatoes',25),('peppers',6)]
    '''segregerate the plants based on fruit and vegetable'''
    vegetable = []
    fruit = []
    for plant in inventory:
        if plant[0] == 'lettuce':
            vegetable.append(plant)
        if plant[0] == 'carrots':
            vegetable.append(plant)
        if plant[0] == 'tomatoes':
            fruit.append(plant)
        if plant[0] == 'peppers':
            fruit.append(plant)

    return vegetable,fruit

'''Function to create the database for the inventory'''
def createInventoryDB():
    db = sqlite3.connect('inventory.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory(Plant TEXT, Quantity INTEGER)''')
    db.commit() # Save (commit) the changes
    ClosingDB(db)

'''Function to fill the database for the inventory'''
def FillInventoryDB():
    db = sqlite3.connect('inventory.db')
    cursor = db.cursor()
    vegetable,fruit = FillInventory()
    for plant in vegetable:
        cursor.execute("INSERT INTO Inventory VALUES(?,?)",plant)
    for plant in fruit:
        cursor.execute("INSERT INTO Inventory VALUES(?,?)",plant)
    db.commit() # Save (commit) the changes
    ClosingDB(db)

'''Function to close the inventory database'''
def ClosingInventoryDB(db):
    db.close()

'''Function to update the inventory database'''
def UpdateInventoryDB(plant,quantity):
    db = sqlite3.connect('inventory.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Inventory WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[1] > 0:
        cursor.execute("UPDATE Inventory SET Quantity = ? WHERE Plant = ?",(row[1]-quantity,plant))
        db.commit()
    ClosingInventoryDB(db)

'''Function to check the inventory database'''
def CheckInventoryDB(plant,quantity):
    db = sqlite3.connect('inventory.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Inventory WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[1] >= quantity:
        return True
    else:
        return False
    ClosingInventoryDB(db)

'''Function to create the database for the plants'''
def createPlantsDB():
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Plants(Plant TEXT, Quantity INTEGER, Growth INTEGER, Status TEXT)''')
    db.commit() # Save (commit) the changes
    ClosingPlantsDB(db)

'''Function to fill the database for the plants'''
def FillPlantsDB():
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    vegetable,fruit = FillInventory()
    for plant in vegetable:
        cursor.execute("INSERT INTO Plants VALUES(?,?,?,?)",(plant[0],plant[1],0,''))
    for plant in fruit:
        cursor.execute("INSERT INTO Plants VALUES(?,?,?,?)",(plant[0],plant[1],0,''))
    db.commit() # Save (commit) the changes
    ClosingPlantsDB(db)

'''Function to close the plants database'''
def ClosingPlantsDB(db):
    db.close()

'''Function to update the plants database'''
def UpdatePlantsDB(plant,quantity):
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Plants WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[1] > 0:
        cursor.execute("UPDATE Plants SET Quantity = ? WHERE Plant = ?",(row[1]-quantity,plant))
        db.commit()
    ClosingPlantsDB(db)

'''Function to check the plants database'''
def CheckPlantsDB(plant,quantity):
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Plants WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[1] >= quantity:
        return True
    else:
        return False
    ClosingPlantsDB(db)

'''Function to update the growth of the plants'''
def UpdateGrowthDB(plant,growth):
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Plants WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[1] > 0:
        cursor.execute("UPDATE Plants SET Growth = ? WHERE Plant = ?",(row[2]+growth,plant))
        db.commit()
    ClosingPlantsDB(db)

'''Function to check the growth of the plants'''
def CheckGrowthDB(plant,growth):
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Plants WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[2] >= growth:
        return True
    else:
        return False
    ClosingPlantsDB(db)

'''Function to update the status of the plants'''
def UpdateStatusDB(plant,status):
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Plants WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[1] > 0:
        cursor.execute("UPDATE Plants SET Status = ? WHERE Plant = ?",(status,plant))
        db.commit()
    ClosingPlantsDB(db)

'''Function to check the status of the plants'''
def CheckStatusDB(plant,status):
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Plants WHERE Plant = ?",(plant,))
    row = cursor.fetchone()
    if row[3] == status:
        return True
    else:
        return False
    ClosingPlantsDB(db)


'''Function PrintInventory to print the inventory'''
'''Create list of Tuples for fruits and vegetables'''
'''Print out this list using pprint'''
def PrintInventory(veteable,fruit):
    vegetable,fruit = FillInventory()
    print('Vegetables')
    pprint.pprint(vegetable)
    print('Fruits')
    pprint.pprint(fruit)
    
'''Function to print the inventory database'''
def PrintInventoryDB():
    db = sqlite3.connect('inventory.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Inventory")
    row = cursor.fetchall()
    print('Inventory')
    pprint.pprint(row)
    ClosingInventoryDB(db)

'''Function to print the plants database'''
def PrintPlantsDB():
    db = sqlite3.connect('plants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Plants")
    row = cursor.fetchall()
    print('Plants')
    pprint.pprint(row)
    ClosingPlantsDB(db)

'''Function to print the greenhouse database'''
def PrintGreenhouseDB():
    db = sqlite3.connect('greenhouse.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Greenhouse")
    row = cursor.fetchall()
    print('Greenhouse')
    pprint.pprint(row)
    ClosingGreenhouseDB(db)

'''Function to print the device counter: number of times the equipment has been used'''
def PrintDeviceCounterDB():
    db = sqlite3.connect('devicecounter.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM DeviceCounter")
    row = cursor.fetchall()
    print('DeviceCounter')
    pprint.pprint(row)
    ClosingDeviceCounterDB(db)

'''Function to add a plant to the dictionary'''
def AddPlant(plants,plant):
    plants[plant] = plant
    return plants

'''Function to remove a plant from the dictionary'''
def RemovePlant(plants,plant):
    del plants[plant]
    return plants

'''Function to count the number of plants in the dictionary'''
def CountPlants(plants):
    count = 0
    for plant in plants:
        count += 1
    return count

'''Function to count the number of plants of a type in the dictionary'''
def CountType(plants,plant):
    count = 0
    for i in plants:
        if plants[i] == plant:
            count += 1
    return count


'''Main function'''
def main():
    '''Create a dictionary of plants'''
    plants = {}
    '''Create a list of Tuples for fruits and vegetables'''
    vegetable,fruit = FillInventory()
    '''Print out this list using pprint'''
    PrintInventory(vegetable,fruit)
    '''Create a database for the inventory'''
    CreateInventoryDB()
    '''Fill the database for the inventory'''
    FillInventoryDB()
    '''Print the database for the inventory'''
    PrintInventoryDB()
    '''Create a database for the plants'''
    CreatePlantsDB()
    '''Fill the database for the plants'''
    FillPlantsDB()
    '''Print the database for the plants'''
    PrintPlantsDB()
    '''Create a database for the greenhouse'''
    CreateGreenhouseDB()
    '''Fill the database for the greenhouse'''
    FillGreenhouseDB()
    '''Print the database for the greenhouse'''
    PrintGreenhouseDB()
    '''Create a database for the device counter'''
    CreateDeviceCounterDB()
    '''Fill the database for the device counter'''
    FillDeviceCounterDB()
    '''Print the database for the device counter'''
    PrintDeviceCounterDB()
    '''Add a plant to the dictionary'''
    plants = AddPlant(plants,'Tomato')
    '''Remove a plant from the dictionary'''
    plants = RemovePlant(plants,'Tomato')
    '''Count the number of plants in the dictionary'''
    count = CountPlants(plants)
    '''Count the number of plants of a type in the dictionary'''
    count = CountType(plants,'Tomato')
    '''Update the plants database'''
    UpdatePlantsDB('Tomato',1)
    '''Check the plants database'''
    CheckPlantsDB('Tomato',1)
    '''Update the growth of the plants'''
    UpdateGrowthDB('Tomato',1)
    '''Check the growth of the plants'''
    CheckGrowthDB('Tomato',1)
    '''Update the status of the plants'''
    UpdateStatusDB('Tomato','Ready')
    '''Check the status of the plants'''
    CheckStatusDB('Tomato','Ready')
    '''Update the inventory database'''
    UpdateInventoryDB('Tomato',1)
    '''Check the inventory database'''
    CheckInventoryDB('Tomato',1)
    '''Update the greenhouse database'''
    UpdateGreenhouseDB('Tomato',1)
    '''Check the greenhouse database'''
    CheckGreenhouseDB('Tomato',1)
    '''Update the device counter database'''
    UpdateDeviceCounterDB('WateringCan',1)
    '''Check the device counter database'''
    CheckDeviceCounterDB('WateringCan',1)
    '''Update the inventory database'''
    UpdateInventoryDB('Tomato',-1)
    '''Check the inventory database'''
    CheckInventoryDB('Tomato',-1)
    '''Update the greenhouse database'''
    UpdateGreenhouseDB('Tomato',-1)
    '''Check the greenhouse database'''
    CheckGreenhouseDB('Tomato',-1)
    '''Update the device counter database'''
    UpdateDeviceCounterDB('WateringCan',-1)
    '''Check the device counter database'''
    CheckDeviceCounterDB('WateringCan',-1)
    '''Update the plants database'''
    UpdatePlantsDB('Tomato',-1)
    '''Check the plants database'''
    CheckPlantsDB('Tomato',-1)
    '''Update the growth of the plants'''
    UpdateGrowthDB('Tomato',-1)
    '''Check the growth of the plants'''
    CheckGrowthDB('Tomato',-1)
    '''Update the status of the plants'''
    UpdateStatusDB('Tomato','Not Ready')
    '''Check the status of the plants'''
    CheckStatusDB('Tomato','Not Ready')
    '''Print the database for the inventory'''
    PrintInventoryDB()
    '''Print the database for the plants'''
    PrintPlantsDB()
    '''Print the database for the greenhouse'''
    PrintGreenhouseDB()
    '''Print the database for the device counter'''
    PrintDeviceCounterDB()
    '''Close the database for the inventory'''
    ClosingInventoryDB(db)
    '''Close the database for the plants'''
    ClosingPlantsDB(db)
    '''Close the database for the greenhouse'''
    ClosingGreenhouseDB(db)
    '''Close the database for the device counter'''
    ClosingDeviceCounterDB(db)

'''close the main function'''





'''Call the main function'''
main()
    

'''close the program'''
