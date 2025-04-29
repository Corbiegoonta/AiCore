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
        dataframe["issue_date"] = dataframe["issue_date"].astype("datetime64[ns]")
        dataframe["earliest_credit_line"] = dataframe["earliest_credit_line"].astype("datetime64[ns]")
        dataframe["last_payment_date"] = dataframe["last_payment_date"].astype("datetime64[ns]")
        dataframe["next_payment_date"] = dataframe["next_payment_date"].astype("datetime64[ns]")
        dataframe["last_credit_pull_date"] = dataframe["last_credit_pull_date"].astype("datetime64[ns]")
        dataframe['term'] = dataframe['term'].str[0:2]
        dataframe['term'] = pd.to_numeric(dataframe['term'], downcast="integer")
        pd.options.display.float_format = '{:.2f}'.format

        return dataframe    

    def drop_colums_with_significant_null_count(self, dataframe, null_percentage_threshold:int):
        threshold = len(dataframe) * null_percentage_threshold / 100
        dataframe.dropna(thresh=threshold, axis=1, inplace=True)

        return dataframe
    
    def impute_columns_with_missing_data(self, dataframe):
        dataframe = DataTransformation.correct_field_data_types(self, dataframe)
        dataframe = DataTransformation.drop_colums_with_significant_null_count(self, dataframe, 30)
        pd.options.display.float_format = '{:.2f}'.format
        dataframe_with_nulls = copy.deepcopy(dataframe)
        columns_to_be_imputed = []
        columns_with_nulls = dataframe.isna()
        df_mean = dataframe.mean(numeric_only=True)
        for column in dataframe:
            if len(columns_with_nulls[column].value_counts().index) == 2:
                if dataframe[column].dtype == int or dataframe[column].dtype == float:
                    columns_to_be_imputed.append(column)
                    dataframe[column].fillna(df_mean[column], inplace=True)
        for row in columns_to_be_imputed:
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
    
    def log_transformation_skew_reduction(self, dataframe, columns):
        for column in columns:
            dataframe[column] = np.log(dataframe[column] + 1)  # Add 1 to avoid log(0)

        return dataframe
    
    def cube_root_transformation_skew_reduction(self, column_skew): # handles both negative and positive values and works for moderate to high skewness.
        column = np.cbrt(column_skew)

        return column

    def yeo_johnson_transformation_skew_reduction(self, column_skew):
        yeo_johnson_transformed, _ = yeojohnson(column_skew)

        return yeo_johnson_transformed
    
    def reduce_skew(self, dataframe: pd.DataFrame):
        skewed_columns = []
        for column in dataframe.columns[1:]:
            if type(dataframe[column].dtypes) == np.dtypes.Float64DType or type(dataframe[column].dtypes) == np.dtypes.Int64DType:
                if "id" not in column:
                    column_skew = dt.correct_skew(dataframe[column])
                    if not dataframe[column].equals(column_skew):
                        skewed_columns.append(column)
                        print(dataframe[column])
                        print(column_skew.skew())
                        col_name = column + "_skew"
                        dataframe[col_name] = column_skew
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
                # Identify outliers (Z > 3 or Z < -3)
                df[col + "_outlier"] = ((df[col_name + "_zscore"] > 3) | (df[col_name + "_zscore"] < -3))
                print(df[col + "_outlier"].value_counts())
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

                # Identify outliers (Z > 3 or Z < -3)
                df[col + "_outlier"] = ((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))
                print(df[col + "_outlier"].value_counts())          
        for col in columns:
            dfc = copy.deepcopy(df)
            o_subset = dfc[col][dfc[col + "_outlier"] == True]
            n_subset = dfc[col][dfc[col + "_outlier"] == False]
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
            plt.figure(figsize=(10, 6))
            plt.scatter(n_subset.index, n_subset, label='Data')
            plt.title(f'Outliers in {col}')
            plt.legend()
            plt.show()

        for col in columns:
            o_subset = df[col][df[col + "_outlier"] == True]
            df.drop(index=o_subset.index, inplace=True)

        return df
    
    def create_correlation_matrix(self, dataframe: pd.DataFrame = None):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dataframe = dataframe_without_nulls
        cols = []
        for column in dataframe.columns[1:-2]:
            if type(dataframe[column].dtypes) == np.dtypes.Float64DType or type(dataframe[column].dtypes) == np.dtypes.Int64DType:
                if "id" not in column:
                    cols.append(column)
        dfn = dataframe[cols]
        corr_df = dfn.corr()
        corr_dft = corr_df[abs(corr_df) > 0.7]
        to_drop = []
        pd.set_option('display.max_rows', None)
        print(corr_dft[~((corr_dft > 0.00) & (corr_dft < 1.00)).any()])
        cdf = corr_dft[((corr_dft > 0.00) & (corr_dft < 1.00)).any(skipna=True)]
        cdf = cdf.dropna(axis=1, how="all")
        columns_to_drop = ["funded_amount_inv", "out_prncp_inv", "total_payment_inv", "instalment"]
        dataframe_without_nulls.drop(columns=columns_to_drop, inplace=True)

        return dataframe_without_nulls
    
    def save_dataframe_to_csv(self, dataframe, file_name: str):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dataframe_with_nulls.to_csv(rf"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\{file_name}", index=False)
        pass    

    def percentage_of_loans_recovered(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        rl = dataframe_without_nulls
        tp = rl["total_payment"] 
        fa = rl["funded_amount"] 
        tri = rl["total_rec_int"]
        t = rl["term"]
        pir = rl["int_rate"]/12

        #((ir / 100 * t) * fa) + fa
        rl["total_calc_6_months"] = (fa*(pir*(1+pir)**(t))/(1+pir)**(t-1))*6
        rl["total"] = rl["term"] * rl["instalment"]
        rlc = rl.loc[rl["loan_status"].isin(["Does not meet the credit policy. Status:Fully Paid", "Fully Paid"])].get(["loan_status", "loan_amount", "funded_amount", "funded_amount_inv", "total_payment", "total_rec_int", "term", "instalment", "int_rate", "total_calc", "total"])
        rlci = rl.loc[~rl["loan_status"].isin(["Does not meet the credit policy. Status:Fully Paid", "Fully Paid"])]
        rlci["amount_to_pay_after_1_months"] = rlci["loan_amount"] - rlci["total_payment"] - rlci["instalment"] 
        rlci["instalment_6_month"] = rlci["instalment"] * 6
        rdf = pd.DataFrame(columns=["month", "total_repayed"])
        month = []
        total = []
        for i in range(1, 7):
            rlci[f"amount_to_pay_after_{i}_months"] = rlci["loan_amount"] - rlci["total_payment"] - (rlci["instalment"] * i)
            rlci[f"cleared_after{i}_months"] = np.where(rlci[f"amount_to_pay_after_{i}_months"] <= 0, True, False)
            month.append(f"month_{i}")
            total.append(len(rlci[rlci[f"cleared_after{i}_months"] == True]))
        rdf["month"] = month
        rdf["total_repayed"] = total

        return rdf

    def charged_off_loans(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        df = dataframe_without_nulls
        coldf = df.loc[df["loan_status"].str.contains("Charged Off") | df["loan_status"].str.contains("Does not meet the credit policy. Status:Charged Off")]
        col = len(coldf)
        al = len(df)
        p = (col / al) * 100
        tp = coldf["total_payment"] 
        tri = coldf["total_rec_int"]
        tc = tp + tri
        coldf["total_collected"] = tc
        ttbp = coldf["instalment"] * coldf["term"]
        coldf["total_to_be_paid"] = ttbp
        coldf["amount_lost"] = ttbp - tc

        fa = df["funded_amount"] 
        t = df["term"]
        pir = df["int_rate"]/12
        df["monthly_payment"] = (fa*(pir*(1+pir)**(t))/(((1+pir)**t)-1)) # avoid
        df["monthly_payment2"] = (fa*pir/(1-(1+pir)**(-t))) # avoid
        df["total_payment_to_date"] = tp + tri
        df["full_payment"] = df["monthly_payment"] * df["term"] # avoid
        df["outstanding_balance"] = df["full_payment"] - df["total_payment_to_date"] # avoid
        df["number_of_months_paid"] = df["total_payment_to_date"] / df["monthly_payment"] # avoid
        df["number_of_months_left"] = df["number_of_months_paid"] - df["term"]
        df["number_of_months_paid1"] = df["total_payment_to_date"] / df["full_payment"] * df["term"] # avoid
        df["number_of_months_left1"] = df["number_of_months_paid1"] - df["term"]
        co = df.loc[df["loan_status"].str.contains("Charged Off") | df["loan_status"].str.contains("Does not meet the credit policy. Status:Charged Off")]
        print(round(p, 3))
        print(tc)
        print(coldf[["total_collected", "total_to_be_paid", "amount_lost"]])

        return df, coldf

    def behind_on_payments(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        df = dataframe_without_nulls
        ldf = df.loc[df["loan_status"].str.contains("Late")]
        pl = len(ldf)/len(df) * 100
        nol = len(ldf)
        ldf["late_loss"] = ldf["instalment"]
        ldf["late_loss_120"] = copy.deepcopy(ldf[ldf["loan_status"].str.contains("120")][["instalment"]] * 4)
        ldf["late_loss_16"] = copy.deepcopy(ldf[ldf["loan_status"].str.contains("30")][["instalment"]])
        print(pl)
        print(nol)
        print(ldf["loan_status"].value_counts())
        print(ldf["late_loss"].value_counts())
        print(ldf.loc[df["loan_status"].str.contains("120")][["loan_status", "instalment", "late_loss_120", "late_loss_16"]])
        late_loss = round(ldf["late_loss_120"].sum() + ldf["late_loss_120"].sum(), 2)
        print(late_loss)

        tp = ldf["total_payment"] 
        tri = ldf["total_rec_int"]
        tc = tp + tri
        ldf["total_collected"] = tc
        ttbp = ldf["instalment"] * ldf["term"]
        ldf["total_to_be_paid"] = ttbp
        ldf["amount_lost"] = ttbp - tc
        loss = ldf["amount_lost"].sum()
        print(round(loss, 2))
        
        coldf = df.loc[df["loan_status"].str.contains("Charged Off") | df["loan_status"].str.contains("Does not meet the credit policy. Status:Charged Off")]
        col = len(coldf)
        al = len(df)
        p = (col / al) * 100
        tp1 = coldf["total_payment"] 
        tri1 = coldf["total_rec_int"]
        tc1 = tp1 + tri1
        coldf["total_collected"] = tc
        ttbp1 = coldf["instalment"] * coldf["term"]
        coldf["total_to_be_paid"] = ttbp1
        coldf["amount_lost"] = ttbp1 - tc1
        coal = coldf["amount_lost"].sum()
        total_loss = coal + loss
        print(round(total_loss, 2))

        totalp = sum(df["total_payment"])
        print(round(totalp, 2))
        full_loss = total_loss / totalp * 100
        print(full_loss)

def indicators_of_loss(self, dataframe):
    dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
    df = dataframe_without_nulls
    pass

class Plotter:

    def __init__(self) -> None:
        pass

    def plot_indicators_of_loss(self, df):
        indicators = ["purpose", "home_ownership", "grade"]
        indicator_dicts = []
        for indicator in indicators:
            idict = dict()
            indicies = list(df[indicator].value_counts().index)
            if indicator == "grade":
                indicies.sort()
            for ind in indicies:
                idict[ind] = []
            indicator_dicts.append(idict)
        statuses = list(df["loan_status"].value_counts().index)
        statuses.remove("Does not meet the credit policy. Status:Fully Paid")
        statuses.remove("Fully Paid")
        statuses.remove("Current")
        statuses.remove("In Grace Period")
        grades = list(df["grade"].value_counts().index)
        purposes = list(df["purpose"].value_counts().index)
        homeowner = list(df["home_ownership"].value_counts().index)
        for stat in statuses:
            data_g = copy.deepcopy(df.loc[df["loan_status"] == stat][indicators[2]].value_counts().sort_index())
            data_p = copy.deepcopy(df.loc[df["loan_status"] == stat][indicators[0]].value_counts().sort_index())
            data_h = copy.deepcopy(df.loc[df["loan_status"] == stat][indicators[1]].value_counts().sort_index())
            data_dict_g = data_g.to_dict()
            data_dict_p = data_p.to_dict()
            data_dict_h = data_h.to_dict()
            for dg in grades:
                if dg not in data_g:
                    data_dict_g[dg] = 0
            for dp in purposes:
                if dp not in data_p:
                    data_dict_p[dp] = 0
            for dh in homeowner:
                if dh not in data_h:
                    data_dict_h[dh] = 0
            data_g = pd.Series(data_dict_g)
            data_p = pd.Series(data_dict_p)
            data_h = pd.Series(data_dict_h)
            data_g.sort_index(inplace=True)
            data_p.sort_index(inplace=True)
            data_h.sort_index(inplace=True)
            for grad, datg in zip(grades, data_g):
                indicator_dicts[2][grad].append(datg)
            for purp, datp in zip(purposes, data_p):
                indicator_dicts[0][purp].append(datp)
            for hou, dath in zip(homeowner, data_h):
                indicator_dicts[1][hou].append(dath)
        for purpo in purposes:
            indicator_dicts[0][purpo] = np.array(indicator_dicts[0][purpo])
        for houseo in homeowner:
            indicator_dicts[1][houseo] = np.array(indicator_dicts[1][houseo])
        for grade in grades:
            indicator_dicts[2][grade] = np.array(indicator_dicts[2][grade])
        width = 0.5
        fig, (grades_axis, purpose_axis, homeowner_axis) = plt.subplots(3)
        bottom_g = np.zeros(len(statuses))
        bottom_p = np.zeros(len(statuses))
        bottom_h = np.zeros(len(statuses))
        for grads, count in indicator_dicts[2].items():
            g = grades_axis.bar(statuses, count, width, label=grads, bottom=bottom_g)
            bottom_g += count
        for purps, count1 in indicator_dicts[0].items():
            p = purpose_axis.bar(statuses, count1, width, label=purps, bottom=bottom_p)
            bottom_p += count
        for hous, count2 in indicator_dicts[1].items():
            h = homeowner_axis.bar(statuses, count2, width, label=hous, bottom=bottom_h)
            bottom_h += count
        grades_axis.set_title("Indicators of Loss (Grades)")
        grades_axis.legend(loc="upper right")
        purpose_axis.set_title("Indicators of Loss (Purpose)")
        purpose_axis.legend(loc="upper right")
        homeowner_axis.set_title("Indicators of Loss (Homeowner)")
        homeowner_axis.legend(loc="upper right")
        plt.show()
        
    
    def create_repayment_plot(self, dataframe):
        print(list(dataframe["term"].values))
        print(list(dataframe["total_repayed"].values))
        dataframe.plot.line(x="month", y="total_repayed")
        plt.show()

    def create_charged_off_plot(self, dataframe, x_axis="term", y_axis="amount_lost"):
        terms = list(dataframe[x_axis].value_counts().index)
        amount_lost = []
        al = 0
        for term in terms:
            al += sum(dataframe[dataframe[x_axis] == term][y_axis])
            amount_lost.append(al)
        new_df = pd.DataFrame({"term": terms, "amount_lost": amount_lost})
        new_df = pd.concat([new_df, pd.DataFrame(new_df.iloc[1]).T])
        new_df.reset_index(drop=True, inplace=True)
        new_df.drop(index=1, inplace=True)
        new_df.reset_index(drop=True, inplace=True)
        print(new_df)
        new_df.plot.line(x="term", y="amount_lost")
        plt.title("Charged Off Loans")
        plt.xlabel("Terms")
        plt.ylabel("Amount Lost")
        plt.show()


    def create_null_plot(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        imputed_cols = []
        if len(dataframe_with_nulls) == len(dataframe_without_nulls):
            for columnwon, columnwn in zip(dataframe_without_nulls.columns, dataframe_with_nulls.columns):
                if not dataframe_without_nulls[columnwon].equals(dataframe_with_nulls[columnwn]):
                    imputed_cols.append(columnwon)
        else:
            print("The lengths of the orginal dataframe and the imputed dataframe are different.")
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
        # Adjust the figure size as needed
        
        # Plot the data
        new_df.plot.bar() # Rotate x-axis labels if needed
        plt.show()
        
    def visualise_outliers_iqr(self, dataframe):
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dfwon = copy.deepcopy(dataframe_without_nulls)
        df, columns = DataTransformation().reduce_skew(dfwon)
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
            # Identify outliers (Z > 3 or Z < -3)
            df[col + "_outlier"] = ((dataframe[col] < lower_bound) | (dataframe[col] > upper_bound))
            print(df[col + "_outlier"].value_counts())        
        for col in columns:
            o_subset = df[col][df[col + "_outlier"] == True]
            plt.figure(figsize=(10, 6))
            plt.scatter(df[col].index, df[col], label='Data')
            plt.scatter(o_subset.index, o_subset, color='red', label='Outliers')
            plt.title(f'Outliers in {col} using Z-score')
            plt.legend()
            plt.show()
    
    def visualise_outliers_z_score(self, dataframe):   
        dataframe_without_nulls, dataframe_with_nulls = DataTransformation().impute_columns_with_missing_data(dataframe)
        dfwon = copy.deepcopy(dataframe_without_nulls)
        df, columns = DataTransformation().reduce_skew(dfwon)
        for col in columns:         
        # Calculate Z-scores
            col_name = col + "_skew"
            df[col_name + "_zscore"] = zscore(df[col_name])
            # Identify outliers (Z > 3 or Z < -3)
            df[col + "_outlier"] = ((df[col_name + "_zscore"] > 3) | (df[col_name + "_zscore"] < -3))
            print(df[col + "_outlier"].value_counts())        
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
    pl.plot_indicators_of_loss(output)

