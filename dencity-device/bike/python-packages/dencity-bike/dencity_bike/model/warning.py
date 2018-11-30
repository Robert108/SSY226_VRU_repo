import json

class Warning:
    "Represents a warning to be shown to a user"
    def __init__(self):
        self._type = "collision"
        self._threat_identifier = "bus"
        self._threat_direction = 0.0
        self._threat_distance = 0.0
        self._priority = "medium"

    @property
    def type(self):
        "Type of warning. Enum('collision'). Default: 'collision'"
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def threat_identifier(self):
        "Identifier for the cause of the threat. Enum('bus'). Default: 'bus'"
        return self._threat_identifier
    
    @threat_identifier.setter
    def threat_identifier(self, value):
        self._threat_identifier = value
    
    @property
    def threat_direction(self):
        "Direction of threat, degrees from current heading. Number. Default: 0.0"
        return self._threat_direction
    
    @threat_direction.setter
    def threat_direction(self, value):
        self._threat_direction = value
    
    @property
    def threat_distance(self):
        "Distance to threat in meters. Number. Default: 0.0"
        return self._threat_distance
    
    @threat_distance.setter
    def threat_distance(self, value):
        self._threat_distance = value
    
    @property
    def priority(self):
        "Priority of warning. Enum('high', 'medium', 'low'). Default: 'medium'"
        return self._priority
    
    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def as_dict(self):
        data = {}
        data['type'] = self.type
        data['threat_direction'] = self.threat_direction
        data['threat_distance'] = self.threat_distance
        data['threat_priority'] = self.priority
        data['threat_identifier'] = self.threat_identifier
        return data

    @property
    def as_json(self):
        return json.dumps(self.as_dict)
