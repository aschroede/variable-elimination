import pandas as pd


class Factor():

    def __init__(self, cpt: pd.DataFrame):
        self.factor = cpt
        assert isinstance(self.factor, pd.DataFrame)

    def reduce_factor(self, variable, value):
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
        self.factor = self.factor.groupby(columns_to_keep).sum().reset_index()

        # Remove variable that has been reduced
        self.factor.drop(variable, axis=1, inplace=True)

    @staticmethod
    def multiply(factor1: "Factor", factor2: "Factor", variable):
        f1_df = factor1.get_data_frame()
        f2_df = factor2.get_data_frame()

        all_columns = f1_df.columns[:].tolist()
        new_factor = pd.merge(f1_df, f2_df, on=variable, suffixes=("_1", "_2"))
        new_factor["prob"] = new_factor["prob_1"]*new_factor["prob_2"]
        new_factor = new_factor[all_columns]

        return new_factor


    def get_data_frame(self):
        return self.factor

# list[

#     tuple{ dictionary{Alarm = True, Buglary = True, Earthquake = True}, 0.95 } 
#     tuple{ dictionary{Alarm = False, Buglary = True, Earthquake = True}, 0.05 }
#     tuple{ dictionary{Alarm = True, Buglary = False, Earthquake = True}, 0.29 }
#     tuple{ dictionary{Alarm = False, Buglary = False, Earthquake = True}, 0.71 }

#     etc    


#     ]
