class Formation:
    """
    The Formation class contains all of the information for a single formation.
    """

    def __init__(self, input_dict=None):
        """
        Initialization function - creates either a blank dict or copies one from input
        Input: Optional formation dictionary
        Output: None  -  the formation is created
        """

        # Create formation from input
        if input_dict is not None:

            # Summary Info
            self.name = input_dict['name']
            self.style = input_dict['style']
            self.description = input_dict['description']
            self.num_links = input_dict['num_links']

            # Position Info
            self.num_defenders = input_dict['num_defenders']
            self.num_midfielders = input_dict['num_midfielders']
            self.num_attackers = input_dict['num_attackers']
            self.positions = input_dict['positions']

    def create_formation(self, name, style, description, num_links,
                         num_defenders, num_midfielders, num_attackers, positions):
        """
        Create a formation manually from the individual components
        Input:
            name: The name of the formation (ex. '4-4-2').
            style: The style of the formation (ex. attacking).
            description: The description of the formation.
            num_links: The total number of connections between players.
            num_defenders: The number of players on defense.
            num_midfielders: The number of players in midfield.
            num_attackers: The number of players on offense.
            positions: A list of all of the dict in the formation.

        For example of input, see NewFormationForm.py

        Output: None  -  the formation is created
        """

        # Assign Info
        self.name = name
        self.style = style
        self.description = description
        self.num_links = num_links
        self.num_defenders = num_defenders
        self.num_midfielders = num_midfielders
        self.num_attackers = num_attackers
        self.positions = positions
