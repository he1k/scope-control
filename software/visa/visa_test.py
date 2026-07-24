import pyvisa
import time
import util

def control_mso2012(resource_name):
    # 1. Initialize the VISA Resource Manager
    rm = pyvisa.ResourceManager()
    
    # Replace this string with your scope's actual VISA address
    #resource_name = 'TCPIP0::192.168.1.50::inst0::INSTR' 
    
    try:
        # Open the connection and set a 5-second timeout
        scope = rm.open_resource(resource_name)
        scope.timeout = 5000 
        
        # 2. Verify communication (Ask the scope to identify itself)
        idn = scope.query('*IDN?')
        print(f"Successfully connected to: {idn.strip()}")
        
        # 3. Reset the scope to a known factory state (Optional but recommended)
        print("Resetting scope...")
        scope.write('*RST')
        scope.write('*CLS') # Clear status registers
        time.sleep(2)       # Give the scope a couple of seconds to process the reset
        
        # 4. Configure Channel 1
        scope.write('SELect:CH1 ON')             # Turn CH1 on
        scope.write('CH1:SCAle 1.0')             # Set vertical scale to 1V / division
        scope.write('TIMebase:MAIN:SCAle 0.001') # Set horizontal scale to 1ms / division
        print("Channel 1 configured.")
        
        # 5. Set up and read a Peak-to-Peak measurement on CH1
        scope.write('MEASUrement:IMMed:TYPe PK2Pk')
        scope.write('MEASUrement:IMMed:SOUrce CH1')
        
        # Wait a brief moment for the scope to capture data and calculate
        time.sleep(1) 
        
        # Query the measurement value
        vpp = scope.query('MEASUrement:IMMed:VALue?')
        print(f"CH1 Peak-to-Peak Voltage: {vpp.strip()} V")
        
    except pyvisa.errors.VisaIOError as e:
        print(f"VISA Error: Could not communicate with the scope.\nDetails: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Always close the connection cleanly
        if 'scope' in locals():
            scope.close()
            print("Connection closed.")

if __name__ == "__main__":
    visa_resource = util.get_visa_resource()
    print('Starting control of MSO2012 with VISA resource string: ', visa_resource)
    control_mso2012(visa_resource)
