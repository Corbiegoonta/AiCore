from data_cleaning import DataTransform as dt
import pandas as pd

class DataFrameInfo:

    def __init__(self) -> None:
        pass

    def describe_df_columns(self, dataframe):
        print("The information for this dataframe is as follows:\n")
        dataframe.info()
        pass

    def show_statistical_df_info(self, dataframe):
        pd.options.display.float_format = '{:.2f}'.format
        print(f"The median values for this dataframe is as follows:\n{dataframe.median()}")    
        print(f"The mean values for this dataframe is as follows:\n{dataframe.mean()}")
        print(f"The standard deviation values for this dataframe is as follows:\n{dataframe.std()}")
        pass

    def show_column_distinct_values(self, dataframe):
        for column in dataframe:
            print(dataframe[column].value_counts())
        pass

    def print_dataframe_shape(self, dataframe):
        print(f"The dataframe has the following shape:\n{dataframe.shape}")
        pass

    def column_null_count(self, dataframe):
        df_showing_nulls = dataframe.isna()
        print("The count of nulls for each column is as follows:\n")
        for column in df_showing_nulls:
            print(df_showing_nulls[column].value_counts())
        print("The proportion of nulls and non_nulls for each column are as follows:\n")
        for column in df_showing_nulls:
            print(df_showing_nulls[column].value_counts(normalize=True))
        pass

    pass