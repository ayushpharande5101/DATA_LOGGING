import time
import pyodbc
from pymodbus.client import ModbusTcpClient
import struct
import datetime

#--------------------------------------------------------------------------------------------------------------------------------
def split_ascii_value(value):
    high_byte = value >> 8
    low_byte = value & 0xFF
    return high_byte, low_byte
#-------------------------------------------------------------------------------------------------------------------------------
def for_list(a):
    result = ""
    for i in a:
        value = i
        high_byte, low_byte = split_ascii_value(value)

        if (65 <= low_byte <= 90 or 48 <= low_byte <= 57) and low_byte != 0:
            result += chr(low_byte)
            #return chr(low_byte)

        if (65 <= high_byte <= 90 or 48 <= high_byte <= 57) and high_byte != 0:
            result += chr(high_byte)
            #return chr(high_byte)
    return result
#--------------------------------------------------------------------------------------------------------------------

def for_list1(a):
    result = ""
    for i in a:
        value = i
        high_byte, low_byte = split_ascii_value(value)

        if (65 <= low_byte <= 90 or 48 <= low_byte <= 57 or low_byte == 32) and low_byte != 0:
            result += chr(low_byte)
            #return chr(low_byte)

        if (65 <= high_byte <= 90 or 48 <= high_byte <= 57 or high_byte == 32) and high_byte != 0:
            result += chr(high_byte)
            #return chr(high_byte)
    return result
#--------------------------------------------------------------------------------------------------------------------

def concatenate(list1):
    if list1[0] < 0:
        a = bin(list1[0])[3:]
        b = bin(list1[1])[2:]
    elif list1[1] < 0:
        a = bin(list1[0])[2:]
        b = bin(list1[1])[3:]
    else:
        a = bin(list1[0])[2:]
        b = bin(list1[1])[2:]

    if list1[0] < 0:
        a = bin(list1[0])[3:]
        b = bin(list1[1])[2:]
    elif list1[1] < 0:
        a = bin(list1[0])[2:]
        b = bin(list1[1])[3:]
    else:
        a = bin(list1[0])[2:]
        b = bin(list1[1])[2:]

    # print(list1)
    # print(a)
    # print(b)

    binary_code = a.zfill(16)
    binary_code1 = b.zfill(16)
    concatenated_binary = binary_code1 + binary_code
    return concatenated_binary
#---------------------------------------------------------------------------------------------------------------------
def binary_to_float_ieee754(binary_string):
    # Convert the binary string to a 32-bit unsigned integer
    ieee754_bits = int(binary_string, 2)

    # Pack the integer into binary data
    packed_data = struct.pack('!I', ieee754_bits)

    # Unpack the binary data as a float number
    float_number = struct.unpack('!f', packed_data)[0]

    return float_number
#-------------------------------------------------------------------------------------------------------------------------

# DATABASE CONNECTION
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                        'Trusted_Connection=yes;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()

table_exists_query = ("IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Data_Log1') "
                      "CREATE TABLE Data_Log1 (DateTime DATETIME, [User] NVARCHAR(50), [Operational Shift] NVARCHAR(50),"
                      " [Station Name] NVARCHAR(50), [Process Name] NVARCHAR(50), [Battery ID] NVARCHAR(50), "
                      "[Cycle Time] INT, [Glue Weight] FLOAT  );")

cursor.execute(table_exists_query)

#---------------------------------------------------------------------------------------------------------------------
# MODBUS SERVER CONNECTION

IP_Address1 = '192.168.10.10'  # 192.168.10.10
IP_Address2 = '192.168.10.11'
IP_Address3 = '192.168.10.12'

#----------------------------------------------------------------------------------------------------------------------
while True:
    if IP_Address1:
        client = ModbusTcpClient(IP_Address1)
        print(client.connect())
        Z = client.read_holding_registers(0, 1)
        print("Value Before Condition: ",Z.registers[0])
        if Z.registers[0] == 1:
            a1 = []
            a2 = []
            a3 = []
            a4 = []
            a5 = []

            b1 = []

            print("Value After: ",Z.registers[0])

            #Values Stored in Registers
            y1 = 1   #1-5 USER
            y2 = 6   #6-10 Operational Shift
            y3 = 11  #11-30 Station Name
            y4 = 31  #31-50 Process Name
            y5 = 51  #51-70 Battery ID
            y6 = 73  #73 Cycle Time
            y7 = 74  #73-74 Glue Weight

            for j1 in range(5):  # LENGTH = 5
                x1 = client.read_holding_registers(y1 + j1, 5)
                A1 = x1.registers[0]
                a1.append(A1)

            for j2 in range(5):  # LENGTH = 5
                x2 = client.read_holding_registers(y2 + j2, 1)
                A2 = x2.registers[0]
                a2.append(A2)

            for j3 in range(20):  # LENGTH = 20
                x3 = client.read_holding_registers(y3 + j3, 25)
                A3 = x3.registers[0]
                a3.append(A3)

            for j4 in range(20):  # LENGTH = 20
                x4 = client.read_holding_registers(y4 + j4, 25)
                A4 = x4.registers[0]
                a4.append(A4)

            for j5 in range(20):  # LENGTH = 20
                x5 = client.read_holding_registers(y5 + j5, 25)
                A5 = x5.registers[0]
                a5.append(A5)

            for n in range(1):  # LENGTH = 2
                x6 = client.read_holding_registers(y6 + n, 2)
                CYCLE_TIME = x6.registers[0]

            for v in range(2):  # LENGTH = 1
                x7 = client.read_holding_registers(y7 + v, 2)
                B7 = x7.registers[0]
                b1.append(B7)

            DATETIME = datetime.datetime.now()  # DateTime
            USER = for_list(a1)
            OPERATIONAL_SHIFT = for_list(a2)
            STATION_NAME = for_list1(a3)
            PROCESS_NAME = for_list1(a4)
            BATTERY_ID = for_list(a5)

            E1 = concatenate(b1)
            GLUE_WEIGHT = binary_to_float_ieee754(E1)

            # print(b1)
            # print(CYCLE_TIME)


            table_name = 'master.dbo.Data_Log1'

            columns = ['DateTime','[User]', '[Operational Shift]', '[Station Name]', '[Process Name]', '[Battery ID]',
                       '[Cycle Time]', '[Glue Weight]']

            values = (DATETIME, USER, OPERATIONAL_SHIFT, STATION_NAME, PROCESS_NAME, BATTERY_ID, CYCLE_TIME, GLUE_WEIGHT )

            SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            cursor.execute(SQLCommand, values)

            print(b1)

            time.sleep(2)
            if f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?,?,?,?,?,?,?,?)":
                print("Data Entered Successfully")
                client.write_registers(0, 0)

            connection.commit()
#=======================================================================================================================

        if IP_Address2:
            client = ModbusTcpClient(IP_Address2)
            print(client.connect())
            Z = client.read_holding_registers(200, 1)
            print("Value Before Condition: ", Z.registers[200])
            if Z.registers[0] == 1:
                a11 = []
                a21 = []
                a31 = []
                a41 = []
                a51 = []

                b11 = []

                print("Value After: ", Z.registers[0])

                # Values Stored in Registers
                y1 = 201  # 1-5 USER
                y2 = 206  # 6-10 Operational Shift
                y3 = 211  # 11-30 Station Name
                y4 = 231  # 31-50 Process Name
                y5 = 251  # 51-70 Battery ID
                y6 = 273  # 73 Cycle Time
                y7 = 274  # 73-74 Glue Weight

                for j1 in range(5):  # LENGTH = 5
                    x1 = client.read_holding_registers(y1 + j1, 5)
                    A1 = x1.registers[0]
                    a11.append(A1)

                for j2 in range(5):  # LENGTH = 5
                    x2 = client.read_holding_registers(y2 + j2, 1)
                    A2 = x2.registers[0]
                    a21.append(A2)

                for j3 in range(20):  # LENGTH = 20
                    x3 = client.read_holding_registers(y3 + j3, 25)
                    A3 = x3.registers[0]
                    a31.append(A3)

                for j4 in range(20):  # LENGTH = 20
                    x4 = client.read_holding_registers(y4 + j4, 25)
                    A4 = x4.registers[0]
                    a41.append(A4)

                for j5 in range(20):  # LENGTH = 20
                    x5 = client.read_holding_registers(y5 + j5, 25)
                    A5 = x5.registers[0]
                    a51.append(A5)

                for n in range(1):  # LENGTH = 2
                    x6 = client.read_holding_registers(y6 + n, 2)
                    CYCLE_TIME = x6.registers[0]

                for v in range(2):  # LENGTH = 1
                    x7 = client.read_holding_registers(y7 + v, 2)
                    B7 = x7.registers[0]
                    b11.append(B7)

                DATETIME = datetime.datetime.now()  # DateTime
                USER = for_list(a11)
                OPERATIONAL_SHIFT = for_list(a21)
                STATION_NAME = for_list1(a31)
                PROCESS_NAME = for_list1(a41)
                BATTERY_ID = for_list(a51)

                E1 = concatenate(b11)
                GLUE_WEIGHT = binary_to_float_ieee754(E1)

                # print(b1)
                # print(CYCLE_TIME)

                table_name = 'master.dbo.Data_Log1'

                columns = ['DateTime', '[User]', '[Operational Shift]', '[Station Name]', '[Process Name]',
                           '[Battery ID]',
                           '[Cycle Time]', '[Glue Weight]']

                values = (
                DATETIME, USER, OPERATIONAL_SHIFT, STATION_NAME, PROCESS_NAME, BATTERY_ID, CYCLE_TIME, GLUE_WEIGHT)

                SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

                cursor.execute(SQLCommand, values)

                time.sleep(2)
                if f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?,?,?,?,?,?,?,?)":
                    print("Data Entered Successfully")
                    client.write_registers(200, 0)

                connection.commit()

# =======================================================================================================================

        if IP_Address3:
            client = ModbusTcpClient(IP_Address3)
            print(client.connect())
            Z = client.read_holding_registers(400, 1)
            print("Value Before Condition: ", Z.registers[400])
            if Z.registers[0] == 1:
                a12 = []
                a22 = []
                a32 = []
                a42 = []
                a52 = []

                b12 = []

                print("Value After: ", Z.registers[0])

                # Values Stored in Registers
                y1 = 401  # 1-5 USER
                y2 = 406  # 6-10 Operational Shift
                y3 = 411  # 11-30 Station Name
                y4 = 431  # 31-50 Process Name
                y5 = 451  # 51-70 Battery ID
                y6 = 473  # 73 Cycle Time
                y7 = 474  # 73-74 Glue Weight

                for j1 in range(5):  # LENGTH = 5
                    x1 = client.read_holding_registers(y1 + j1, 5)
                    A1 = x1.registers[0]
                    a12.append(A1)

                for j2 in range(5):  # LENGTH = 5
                    x2 = client.read_holding_registers(y2 + j2, 1)
                    A2 = x2.registers[0]
                    a22.append(A2)

                for j3 in range(20):  # LENGTH = 20
                    x3 = client.read_holding_registers(y3 + j3, 25)
                    A3 = x3.registers[0]
                    a32.append(A3)

                for j4 in range(20):  # LENGTH = 20
                    x4 = client.read_holding_registers(y4 + j4, 25)
                    A4 = x4.registers[0]
                    a42.append(A4)

                for j5 in range(20):  # LENGTH = 20
                    x5 = client.read_holding_registers(y5 + j5, 25)
                    A5 = x5.registers[0]
                    a52.append(A5)

                for n in range(1):  # LENGTH = 2
                    x6 = client.read_holding_registers(y6 + n, 2)
                    CYCLE_TIME = x6.registers[0]

                for v in range(2):  # LENGTH = 1
                    x7 = client.read_holding_registers(y7 + v, 2)
                    B7 = x7.registers[0]
                    b12.append(B7)

                DATETIME = datetime.datetime.now()  # DateTime
                USER = for_list(a12)
                OPERATIONAL_SHIFT = for_list(a22)
                STATION_NAME = for_list1(a32)
                PROCESS_NAME = for_list1(a42)
                BATTERY_ID = for_list(a52)

                E1 = concatenate(b12)
                GLUE_WEIGHT = binary_to_float_ieee754(E1)

                # print(b1)
                # print(CYCLE_TIME)

                table_name = 'master.dbo.Data_Log1'

                columns = ['DateTime', '[User]', '[Operational Shift]', '[Station Name]', '[Process Name]',
                           '[Battery ID]',
                           '[Cycle Time]', '[Glue Weight]']

                values = (
                DATETIME, USER, OPERATIONAL_SHIFT, STATION_NAME, PROCESS_NAME, BATTERY_ID, CYCLE_TIME, GLUE_WEIGHT)

                SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

                cursor.execute(SQLCommand, values)

                time.sleep(2)
                if f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?,?,?,?,?,?,?,?)":
                    print("Data Entered Successfully")
                    client.write_registers(400, 0)

                connection.commit()


