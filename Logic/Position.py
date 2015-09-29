class Position:
    """
    The Position class contains all of an individual position in a formation.
    """

    def __init__(self, input_dict):
        """
        Initialization function - copies a dict from input.
        Input: Position dictionary.
        Output: None  -  the position is created.
        """

        # Create formation from input
        # Summary Info
        self.name = input_dict['name']
        self.symbol = input_dict['symbol']
        self.custom_symbol = input_dict['custom_symbol']

        # Connection Info
        self.connections = input_dict['connections']
