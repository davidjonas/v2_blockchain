contract mortal {
    address owner;
    function mortal() 
    {
        owner = msg.sender; 
    }
    function kill() { if (msg.sender == owner) suicide(owner); }
}

contract sensor is mortal {
    struct Measurement 
    {
        uint temperature;
        uint humidity;
        uint pressure;
        bool exists;
    }
    
    mapping (address => Measurement) public measurements;
    address[] public sensors;
    
    event NewMeasurement(address sensorNode, uint temperature, uint humidity, uint pressure);
    
    function sendMeasurement(uint temperature, uint humidity, uint pressure)
    {
        NewMeasurement(msg.sender, temperature, humidity, pressure);
        
        measurements[msg.sender] = Measurement(temperature, humidity, pressure, true);
        
        if(!measurements[msg.sender].exists)
        {
            //sensors.push(msg.sender);
        }
        
    }
    
    function getMeasurement(address sensorNode) returns (uint t, uint h, uint p)
    {
        if(measurements[sensorNode].exists)
        {
            t = measurements[sensorNode].temperature;
            h = measurements[sensorNode].humidity;
            p = measurements[sensorNode].pressure;
            
            return;
        }
        else
        {
            throw;
        }
    }
}