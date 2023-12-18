"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from factor import Factor
from read_bayesnet import BayesNet
from logger import logger


class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, query, observed: dict, elim_order):
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
        # Somehow get data into factors that support reduction, maximisation, and marginalization

        logger.info("Query Variables: " + query)
        logger.info("Observed Variables: " + str(observed))
        logger.info("Elimination Order: " + str(elim_order))

        assert isinstance(self.network, BayesNet)
        factors = get_factors_from_cpts(self.network.probabilities)

        logger.info("Original Factors: ")
        self.log_factors(factors)

        # Clamp evidence in the factors
        to_delete = []
        for variable, value in observed.items():
            for factor in factors:
                if variable in factor.get_vars():
                    factor.reduce(variable, value)
                    # Check if factor is trivial
                    if factor.get_data_frame().columns[:].tolist() == ["prob"]:
                        to_delete.append(factor)

        for factor in to_delete:
            factors.remove(factor)

        logger.info("\nFactors with evidence applied: ")
        self.log_factors(factors)


        # Use provided elimination order
        for var_to_eliminate in elim_order:

            logger.info("Eliminate variable: " + var_to_eliminate)

            # Collect all factors to be multiplied
            to_multiply = [factor for factor in factors if any(var == var_to_eliminate for var in factor.get_vars())]
            logger.info("Factors to multiply containing variable: " + var_to_eliminate)
            self.log_factors(to_multiply)

            # Multiply together
            result = to_multiply[0]
            for factor in to_multiply[1:]:
                result = result.multiply(factor, var_to_eliminate)
            
            logger.info("Result of multiplication: ")
            self.log_factor(result)


            # Marginalize
            result = result.marginalize(var_to_eliminate)

            logger.info("Sum out " + var_to_eliminate)
            self.log_factor(result)


            # Remove used factors and replace with new one in list of factors
            for factor in to_multiply:
                factors.remove(factor)
            factors.append(result)

            logger.info("New List of Factors: ")
            self.log_factors(factors)

        logger.info("Elimination step complete. Multiply the following remaining factors together.")
        
        if len(factors) > 1:
            self.log_factors(factors)
        else:
            self.log_factor(factor)

        # Multiply remaining factors
        result = factors[0]
        if len(factors) > 1:
            for factor in factors[1:]:
                result = result.multiply(factor, query)

        logger.info("Final factor pre-normalization.")
        self.log_factor(result)

        # Need to normalize as well
        result.normalize()

        logger.info("Final factor post-normalization.")
        self.log_factor(result)

        return result

    def log_factors(self, factors):
        for factor in factors:
            logger.info('\t'+ factor.get_data_frame().to_string().replace('\n', '\n\t'))

    def log_factor(self, factor):
        logger.info('\t'+ factor.get_data_frame().to_string().replace('\n', '\n\t'))


def get_factors_from_cpts(probabilities):
    factors = []
    for name, cpt in probabilities.items():
        factors.append(Factor(cpt))

    return factors
