class LocationNormalizer:
    def __init__(self, abnormal_location_definition: str):
        self.location_definition = abnormal_location_definition.replace(" ","")
        self.location_list = []
        if self.location_definition is not None:
            self.location_list = self.location_definition.split(',')

    def normalize(self, candidate_name: str):
        count = 0
        normalized_location = None
        lower_candidate_name = candidate_name.lower()
        for location in self.location_list:
            if location.lower().startswith(lower_candidate_name):
                count += 1
                if count > 1:
                    return None
                normalized_location = location
        return normalized_location

