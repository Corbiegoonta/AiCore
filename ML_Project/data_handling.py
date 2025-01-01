from db_utils import RDSDatabaseConnector 
from data_info import DataFrameInfo
from sklearn.preprocessing import PowerTransformer
from scipy.stats import yeojohnson
from scipy.stats import zscore
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
import math


class DataTransformation:

    def __init__(self):
        self.db = RDSDatabaseConnector()
        pass

    def correct_field_data_types(self, dataframe):
        # print(loan_data.mths_since_last_record.value_counts())
        # print(loan_data.issue_date.value_counts())
        dataframe["issue_date"] = dataframe["issue_date"].astype("datetime64[ns]")
        dataframe["earliest_credit_line"] = dataframe["earliest_credit_line"].astype("datetime64[ns]")
        dataframe["last_payment_date"] = dataframe["last_payment_date"].astype("datetime64[ns]")
        dataframe["next_payment_date"] = dataframe["next_payment_date"].astype("datetime64[ns]")
        dataframe["last_credit_pull_date"] = dataframe["last_credit_pull_date"].astype("datetime64[ns]")
        # print(loan_data.issue_date)
        # dates = [issue_date, earliest_credit_line, last_payment_date, next_payment_date, last_credit_pull_date]
        # print(loan_data.columns.values)
        # print(loan_data.loc[0])
        # loan_data.dropna()
        # loan_data.info()
        # loan_data.astype({"loan_amount": float})
        # print(loan_data.term.value_counts())
        dataframe['term'] = dataframe['term'].str[0:2]
        # loan_data.dropna()
        # print(loan_data.term.value_counts())
        dataframe['term'] = pd.to_numeric(dataframe['term'], downcast="integer")
        # loan_data.info()
        pd.options.display.float_format = '{:.2f}'.format
        # print(loan_data.shape)
        # print(loan_data.isna())
        # a = loan_data.isna()
        # for i in a:
        #     print(a[i].value_counts(sort=False))
        # print(loan_data.std())
        # print(loan_data.mths_since_last_major_derog.value_counts())
        # print(loan_data)
        return dataframe
    
    # def number_of_nulls(self, dataframe):
    #     for row in dataframe:
    #         if 
    #         print(dataframe[row].isna().value_counts(sort=False))
    #     pass
    
    pass

    def drop_colums_with_significant_null_count(self, dataframe, null_percentage_threshold:int):
        threshold = len(dataframe) * null_percentage_threshold / 100
        dataframe.dropna(thresh=threshold, axis=1, inplace=True)

        return dataframe
    
    def impute_columns_with_missing_data(self, dataframe):
        dataframe = DataTransformation.correct_field_data_types(self, dataframe)
        dataframe = DataTransformation.drop_colums_with_significant_null_count(self, dataframe, 30)
        # dataframe = dataframe.drop("Unnamed: 0", inplace=True, axis=column)
        pd.options.display.float_format = '{:.2f}'.format
        dataframe_with_nulls = copy.deepcopy(dataframe)
        columns_to_be_imputed = []
        columns_with_nulls = dataframe.isna()
        df_mean = dataframe.mean(numeric_only=True)
        # print(columns_with_nulls['recoveries'].value_counts().index[0])
        # print(dataframe.isna().value_counts())
        # print(dataframe.mean(numeric_only=True))
        # print(type(dataframe.mean(numeric_only=True)))
        # print(dataframe['term'].info)

        # for row in dataframe.isna():
        #     print(dataframe.isna()[row].value_counts())
        for column in dataframe:
            # print(dataframe[column].dtype)
            if len(columns_with_nulls[column].value_counts().index) == 2:
                if dataframe[column].dtype == int or dataframe[column].dtype == float:
                    columns_to_be_imputed.append(column)
                    # print(column) 
                    dataframe[column].fillna(df_mean[column], inplace=True)
        # print(columns_to_be_imputed)
        # print(dataframe.loc[:, columns_to_be_imputed])
        for row in columns_to_be_imputed:
            # print(dataframe.isna()[row].value_counts())

                # print(column)
                # df_col_mean = df_mean[column]
                # print(df_col_mean)
                # print(dataframe.mean(numeric_only=True).index)  

                # dataframe.loc[columns_with_nulls[column].value_counts()] = dataframe[column].mean()
            pass

        return dataframe, dataframe_with_nulls
    
    def correct_skew(self, column: pd.Series):
            skew = column.skew()
            if abs(skew) <= 0.5:
                print(f"The skew on the {column.name} column is minimal therefore no transformation is required.")
                return column
            elif abs(skew) > 0.5 and abs(skew) <= 1: 
                print(f"The skew on the {column.name} column is moderate therefore the Yeo-Johnson transformation will be applied.")
                reduced_skew = dt.yeo_johnson_transformation_skew_reduction(pd.DataFrame(column))
                reduced_skew = pd.DataFrame(data=reduced_skew, columns=[column.name])[column.name]
                print("rsvc")
                print(reduced_skew.value_counts())
                return reduced_skew
            elif abs(skew) > 1:
                print(f"The skew on the {column.name} column is high or extreme therefore the cube-root transformation will be applied.")
                reduced_skew = dt.cube_root_transformation_skew_reduction(pd.DataFrame(column)) 
                print("rsvc")
                print(reduced_skew.value_counts())
                return reduced_skew
            else:
                print(f"The {column.name} column is not of the right data type to apply a skew")
                return column
        # else:
        #     print(f"The {column.name} column is not of the right data type to apply a skew")
        # skew = dataframe.skew(numeric_only=True)
        # skew.drop("Unnamed: 0", inplace=True)
        # skew.drop("id", inplace=True)
        # skew.drop("member_id", inplace=True)
        # minimally_skewed = skew[abs(skew) <= 0.5]
        # moderately_skewed = skew[(abs(skew) > 0.5) & (abs(skew) <= 1)]
        # highly_skewed = skew[(abs(skew) > 1) & (abs(skew) < 3)]
        # extremely_skewed = skew[abs(skew) >= 3]

        # return minimally_skewed, moderately_skewed, highly_skewed, extremely_skewed, skew
    
    def log_transformation_skew_reduction(self, dataframe, columns):
        for column in columns:
            # print("OLD COLUMN")
            # print(dataframe[column])
            dataframe[column] = np.log(dataframe[column] + 1)  # Add 1 to avoid log(0)
            # print("NEW COLUMN")
            # print(dataframe[column])
        # for row in range(len(dataframe[column_name])):
        #     dataframe['log_transformed'] = np.log((row) + 1)  # Add 1 to avoid log(0)
            # print(dataframe['log_transformed'])
        # print(dataframe['log_transformed'])
        return dataframe
    
    def cube_root_transformation_skew_reduction(self, column_skew): # handles both negative and positive values and works for moderate to high skewness.
        # print("OLD SKEW")
        # print(column_skew)
        column = np.cbrt(column_skew)
        # print("NEW SKEW")
        # print(column_skew)
        
        return column

    def yeo_johnson_transformation_skew_reduction(self, column_skew):
        # print("OLD SKEW")
        # print(column_skew)
        yeo_johnson_transformed, _ = yeojohnson(column_skew)
        # print("NEW SKEW")
        # print(column_skew)
        return yeo_johnson_transformed
    
    def reduce_skew(self, dataframe: pd.DataFrame):
        # print(dataframe.columns)
        skewed_columns = []
        for column in dataframe.columns[1:]:
            if type(dataframe[column].dtypes) == np.dtypes.Float64DType or type(dataframe[column].dtypes) == np.dtypes.Int64DType:
                # print(type(dataframe[column].dtypes))
                if "id" not in column:
                    # print(column)
                    # print(dataframe[column].skew())
                    column_skew = dt.correct_skew(dataframe[column])
                    if not dataframe[column].equals(column_skew):
                        skewed_columns.append(column)
                        # print(type(dataframe[column]))
                        # print(type(column_skew))
                        # print(dataframe[column])
                        # print(column_skew)
                        print(dataframe[column])
                        print(column_skew.skew())
                        col_name = column + "_skew"
                        dataframe[col_name] = column_skew
                        # print(dataframe[column])
                    # print(column_skew)
                    # pass
            else:
                continue

        return dataframe, skewed_columns
    
    def remove_outliers(self, dataframe: pd.DataFrame, outlier_type: str = "z_score"):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dfwon = copy.deepcopy(dataframe_without_nulls)
        df, columns = DataTransformation().reduce_skew(dfwon)
        if outlier_type == "z_score":
            for col in columns:         
                # Calculate Z-scores
                col_name = col + "_skew"
                df[col_name + "_zscore"] = zscore(df[col_name])
                # print(type(z))
                # print(z)
                # Identify outliers (Z > 3 or Z < -3)
                df[col + "_outlier"] = ((df[col_name + "_zscore"] > 3) | (df[col_name + "_zscore"] < -3))
                print(df[col + "_outlier"].value_counts())
            # df["outlier"] = df[col_name + "_zscore"][(df[col_name] > 3) | (df[col_name] < -3)]
                # outliers[col] = outl
            # print(df)
            # for i in outliers:
            #     print(len(outliers[i]))


        elif outlier_type == "iqr":
            for col in columns:
                # Calculate Q1, Q3, and IQR
                q1 = dataframe[col].quantile(0.25)
                q3 = dataframe[col].quantile(0.75)
                iqr = q3 - q1

                # Define outlier bounds
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                # Find outliers
                outl = dataframe[col][(dataframe[col] < lower_bound) | (dataframe[col] > upper_bound)]
                noutl = dataframe[col][~((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))]
                col_name = col + "_skew"
                # print(type(z))
                # print(z)
                # Identify outliers (Z > 3 or Z < -3)
                df[col + "_outlier"] = ((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))
                print(df[col + "_outlier"].value_counts())
            # df["outlier"] = df[col_name + "_zscore"][(df[col_name] > 3) | (df[col_name] < -3)]
                # outliers[col] = outl
            # print(df)
            # for i in outliers:
            #     print(len(outliers[i]))
    
        
        for col in columns:
            dfc = copy.deepcopy(df)
            o_subset = dfc[col][dfc[col + "_outlier"] == True]
            n_subset = dfc[col][dfc[col + "_outlier"] == False]
            # dfc = dfc.drop(o_subset.index)
            plt.figure(figsize=(10, 6))
            plt.scatter(n_subset.index, n_subset, label='Data')
            plt.scatter(o_subset.index, o_subset, color='red', label='Outliers')
            plt.title(f'Outliers in {col}')
            plt.legend()
            plt.show()
        
        for col in columns:
            dfc = copy.deepcopy(df)
            n_subset = dfc[col][dfc[col + "_outlier"] == False]
            o_subset = dfc[col][dfc[col + "_outlier"] == True]
            # dfc = dfc.drop(o_subset.index)
            plt.figure(figsize=(10, 6))
            plt.scatter(n_subset.index, n_subset, label='Data')
            # plt.scatter(o_subset.index, o_subset, color='red', label='Outliers')
            plt.title(f'Outliers in {col}')
            plt.legend()
            plt.show()

        for col in columns:
            o_subset = df[col][df[col + "_outlier"] == True]
            df.drop(index=o_subset.index, inplace=True)
        # # col = "loan_amount"
        # for col in columns:
        #     # Calculate Q1, Q3, and IQR
        #     q1 = dataframe[col].quantile(0.25)
        #     q3 = dataframe[col].quantile(0.75)
        #     iqr = q3 - q1

        #     # Define outlier bounds
        #     lower_bound = q1 - 1.5 * iqr
        #     upper_bound = q3 + 1.5 * iqr

        #     # Find outliers
        #     outl = dataframe[col][(dataframe[col] < lower_bound) | (dataframe[col] > upper_bound)]
        #     noutl = dataframe[col][~((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))]
        #     outliers += list(outl.index)
        #     print(len(outliers))

        # # for col, outlier_df in outliers.items():
        
        # # print(len(outliers))
        # outliers = set(outliers)
        # df = df.drop(outliers)
        # # print(len(outliers))
        # # return outliers["loan_amount"]
        return df
    
    def create_correlation_matrix(self, dataframe: pd.DataFrame = None):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dataframe = dataframe_without_nulls
        # print(dataframe["policy_code"].value_counts())
        cols = []
        for column in dataframe.columns[1:-2]:
            if type(dataframe[column].dtypes) == np.dtypes.Float64DType or type(dataframe[column].dtypes) == np.dtypes.Int64DType:
                # print(type(dataframe[column].dtypes))
                if "id" not in column:
                    cols.append(column)
        # print(dataframe[cols])
        dfn = dataframe[cols]
        corr_df = dfn.corr()
        corr_dft = corr_df[abs(corr_df) > 0.7]
        # print(corr_df)
        # print(corr_dft)
        # print(corr_dft.value_counts())
        # print(corr_dft.columns)
        # print(type(corr_dft.columns))
        to_drop = []
        pd.set_option('display.max_rows', None)
        print(corr_dft[~((corr_dft > 0.00) & (corr_dft < 1.00)).any()])
        cdf = corr_dft[((corr_dft > 0.00) & (corr_dft < 1.00)).any(skipna=True)]
        cdf = cdf.dropna(axis=1, how="all")
        columns_to_drop = ["funded_amount_inv", "out_prncp_inv", "total_payment_inv", "instalment"]
        dataframe_without_nulls.drop(columns=columns_to_drop, inplace=True)
        # cdf.to_csv(rf"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\corr.csv")
        # for i in list(corr_dft.columns):
        #     print(None)
            # print(corr_df[~((corr_df[i] > 0.00) | (corr_df[i] < 1.00)).any()])
            # corr_df.drop(corr_df[~((corr_df[i] > 0.00) | (corr_df[i] < 1.00))].index, inplace=True)
            # for j in corr_dft[i]:
            #     # print(type(j))
            #     if j > 0.00 or j < 1.00:
            #         # print("hi")
            #         to_drop.append(i)
        # corr_dft.drop(columns=to_drop, inplace=True)
        # print(corr_dft.value_counts())
        # print(corr_dft)

        return dataframe_without_nulls
    
    def save_dataframe_to_csv(self, dataframe, file_name: str):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dataframe_with_nulls.to_csv(rf"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\{file_name}", index=False)
        pass    

class Plotter:

    def __init__(self) -> None:
        pass

    def create_null_plot(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        imputed_cols = []
        if len(dataframe_with_nulls) == len(dataframe_without_nulls):
            for columnwon, columnwn in zip(dataframe_without_nulls.columns, dataframe_with_nulls.columns):
                if not dataframe_without_nulls[columnwon].equals(dataframe_with_nulls[columnwn]):
                    imputed_cols.append(columnwon)
        else:
            print("The lengths of the orginal dataframe and the imputed dataframe are different.")
        # print(imputed_cols)
        # imputed_cols = ['funded_amount', 'int_rate', 'mths_since_last_delinq', 'mths_since_last_record', 'collections_12_mths_ex_med', 'mths_since_last_major_derog']
        null_count = []
        imputed_null_count = []
        for row in imputed_cols:
            null_count.append(54231 - dataframe_with_nulls.isna()[row].value_counts()[0])
            imputed_null_count.append(54231 - dataframe_without_nulls.isna()[row].value_counts()[0])
        nulls = {}
        nulls["null_count"] = null_count
        nulls["imputed_null_count"] = imputed_null_count
        new_df = pd.DataFrame(nulls, index=imputed_cols)
        new_df.plot.line()
        plt.show()
        pass

    def create_skew_plot(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dfwon = copy.deepcopy(dataframe_without_nulls)
        df, columns = DataTransformation().reduce_skew(dfwon)
        # print(columns)
        skew_before = []
        skew_after = []
        for column in columns:
            skew_before.append(dataframe_without_nulls[column].skew())
            skew_after.append(df[column].skew())
        skews = {}
        skews["before"] = skew_before
        skews["after"] = skew_after
        new_df = pd.DataFrame(skews, index=columns)
        # pd.set_option('display.max_rows', None)
        # print(new_df)
        # Adjust the figure size as needed
        
        # Plot the data
        new_df.plot.bar() # Rotate x-axis labels if needed
        plt.show()
        # low_skew, moderate_skew, high_skew, all_skews = DataTransformation().determine_skewness(DataTransformation().impute_columns_with_missing_data(dataframe)[0])
        # skew_df = pd.DataFrame({"low_skew": low_skew, "moderate_skew": moderate_skew, "high_skew": high_skew})
        # skew_df.plot.line()
        # print(all_skews)
        # plt.plot(low_skew)
        # plt.plot(moderate_skew)
        # print(len(high_skew))
        # plt.plot(high_skew)
        # plt.show()
        
    def visualise_outliers_iqr(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dfwon = copy.deepcopy(dataframe_without_nulls)
        df, columns = DataTransformation().reduce_skew(dfwon)
        # col = "loan_amount"
        for col in columns:
            # Calculate Q1, Q3, and IQR
            q1 = dataframe[col].quantile(0.25)
            q3 = dataframe[col].quantile(0.75)
            iqr = q3 - q1

            # Define outlier bounds
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Find outliers
            outl = dataframe[col][(dataframe[col] < lower_bound) | (dataframe[col] > upper_bound)]
            noutl = dataframe[col][~((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))]
            col_name = col + "_skew"
            # print(type(z))
            # print(z)
            # Identify outliers (Z > 3 or Z < -3)
            df[col + "_outlier"] = ((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))
            print(df[col + "_outlier"].value_counts())
        # df["outlier"] = df[col_name + "_zscore"][(df[col_name] > 3) | (df[col_name] < -3)]
            # outliers[col] = outl
        # print(df)
        # for i in outliers:
        #     print(len(outliers[i]))
        
        for col in columns:
            o_subset = df[col][df[col + "_outlier"] == True]
            plt.figure(figsize=(10, 6))
            plt.scatter(df[col].index, df[col], label='Data')
            plt.scatter(o_subset.index, o_subset, color='red', label='Outliers')
            plt.title(f'Outliers in {col} using Z-score')
            plt.legend()
            plt.show()
        # outl = dataframe[col][(dataframe[col] < lower_bound) | (dataframe[col] > upper_bound)]
        # noutl = dataframe[col][~((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))]
        # print(q1)
        # print(upper_bound)
        # print(lower_bound)
        # print(outl)
        # print(noutl)
        # print(len(dataframe[col]))
        # print(len(outl + noutl))
        # print(np.average(dataframe[col]))
            # outliers[col] = outl
            # print(outliers)
    
    def visualise_outliers_z_score(self, dataframe):   
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dfwon = copy.deepcopy(dataframe_without_nulls)
        df, columns = DataTransformation().reduce_skew(dfwon)
        # outliers = {}
        # zdf = pd.DataFrame()    
        # col = "loan_amount"
        # print(df[col])
        # print(df[col + "_skew"])
        for col in columns:         
        # Calculate Z-scores
            col_name = col + "_skew"
            df[col_name + "_zscore"] = zscore(df[col_name])
            # print(type(z))
            # print(z)
            # Identify outliers (Z > 3 or Z < -3)
            df[col + "_outlier"] = ((df[col_name + "_zscore"] > 3) | (df[col_name + "_zscore"] < -3))
            print(df[col + "_outlier"].value_counts())
        # df["outlier"] = df[col_name + "_zscore"][(df[col_name] > 3) | (df[col_name] < -3)]
            # outliers[col] = outl
        # print(df)
        # for i in outliers:
        #     print(len(outliers[i]))
        
        for col in columns:
            o_subset = df[col][df[col + "_outlier"] == True]
            plt.figure(figsize=(10, 6))
            plt.scatter(df[col].index, df[col], label='Data')
            plt.scatter(o_subset.index, o_subset, color='red', label='Outliers')
            plt.title(f'Outliers in {col} using Z-score')
            plt.legend()
            plt.show()
        pass

    def visualise_correlation(self, dataframe):
        dataframe = dt.create_correlation_matrix(dataframe)
        plt.figure(figsize=(12, 10))
        sns.heatmap(dataframe, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Matrix Heatmap')
        plt.show()

if __name__ == "__main__":
    dt = DataTransformation()
    pl = Plotter()
    output = RDSDatabaseConnector().load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv")
    # out = dt.remove_outliers(output)
    # print(out)
    # pl.visualise_outliers_iqr(out)
    # pl.visualise_outliers_iqr(output)
    # pl.visualise_outliers_z_score(output)
    # dt.remove_outliers(output)
    dt.create_correlation_matrix(output)
    # pl.visualise_correlation(output)
    # pl.create_skew_plot(RDSDatabaseConnector().load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv"))
    # print(dt.reduce_skew(output).info())
    # print(len(output[0]))
    # print(len(output[1]))
    # if type(output["int_rate"].dtype) == np.dtypes.Float64DType or type(output["int_rate"].dtype) == np.dtypes.Int64DType:
    #     print(type(output["int_rate"].dtype))
    # print(list(dt.determine_skewness(output)[1].keys()))
    # skewness = dt.determine_skewness(output)
    # dt.log_transformation_skew_reduction(output, column)
    # for column in skewness[0].keys():
        # print(column)
    # dt.log_transformation_skew_reduction(output, skewness[0].keys())
    # print(output[0].dtypes)
    # count = 0
    # for i in dt.determine_skewness(output):
    #     count += 1
    #     print(count)
    #     print(i)
    # print(dt.determine_skewness(output[0])[2])
    # pl.create_skew_plot(RDSDatabaseConnector().load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv"))
    # DataFrameInfo().column_null_count(nndf)
    # print(list(RDSDatabaseConnector().load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv").columns)[1:])
    # Plotter().create_null_plot(RDSDatabaseConnector().load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv"))
    # DataTransformation().save_dataframe_to_csv(RDSDatabaseConnector().load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv"), "loan_payments_transformed.csv")
    pass

