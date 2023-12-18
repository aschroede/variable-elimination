import pandas as pd


class Factor:

    def __init__(self, cpt: pd.DataFrame):
        self.factor = cpt
        assert isinstance(self.factor, pd.DataFrame)

    def reduce(self, variable, value):
        # Reduce table
        self.factor = self.factor[self.factor[variable] == value]

        # Remove variable that has been reduced
        self.factor.drop(variable, axis=1, inplace=True)

    def marginalize(self, variable):

        # Extract all variable columns (don't select last column which is probability column)
        all_columns = self.factor.columns[:-1]

        # Get all columns except for the column to be marginalized out
        columns_to_keep = [col for col in all_columns if col != variable]

        # Marginalize and reset index
        newFactor = self.factor.groupby(columns_to_keep).sum().reset_index()

        # Remove variable that has been reduced
        newFactor.drop(variable, axis=1, inplace=True)

        return Factor(newFactor)

    def multiply(self, factor2: "Factor", variable):

        f1_df = self.get_data_frame()
        f2_df = factor2.get_data_frame()

        all_columns = f1_df.columns[:-1].tolist() + f2_df.columns[:-1].tolist()
        all_columns = list(set(all_columns))
        all_columns = all_columns + ["prob"]

        new_factor = pd.merge(f1_df, f2_df, on=variable, suffixes=("_1", "_2"))
        new_factor["prob"] = new_factor["prob_1"]*new_factor["prob_2"]
        new_factor = new_factor[all_columns]

        return Factor(new_factor)

    def normalize(self):
        self.factor = self.factor["prob"]/self.factor["prob"].sum()

    def get_data_frame(self):
        return self.factor

    def get_vars(self):
        return self.factor.columns[:].tolist()
    
    def __str__(self) -> str:
        return str(self.get_vars())

# list
