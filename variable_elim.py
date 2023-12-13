"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""

class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
        # 0. Somehow get data into factors that support reduction, maximisation, and marginalization
        # 1. Clamp evidence in the factors
        # 2. Use provided elimination order
        # 3. For each variable in the elimination order
        #   3.1 Multiply all factors that have that variable
        #   3.2 Sum out the variable from the multiplied factor
        # 4. Multiply all remaining factors
        # 5. Normalize

