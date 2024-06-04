from db_utils import RDSDatabaseConnector 
import pandas as pd

class DataTransform:

    def __init__(self):
        self.db = RDSDatabaseConnector()
        pass

    def correct_field_data_types(self):
        loan_data = self.db.load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv")
        # print(loan_data.mths_since_last_record.value_counts())
        # print(loan_data.issue_date.value_counts())
        loan_data["issue_date"] = loan_data["issue_date"].astype("datetime64[ns]")
        loan_data["earliest_credit_line"] = loan_data["earliest_credit_line"].astype("datetime64[ns]")
        loan_data["last_payment_date"] = loan_data["last_payment_date"].astype("datetime64[ns]")
        loan_data["next_payment_date"] = loan_data["next_payment_date"].astype("datetime64[ns]")
        loan_data["last_credit_pull_date"] = loan_data["last_credit_pull_date"].astype("datetime64[ns]")
        # print(loan_data.issue_date)
        # dates = [issue_date, earliest_credit_line, last_payment_date, next_payment_date, last_credit_pull_date]
        # print(loan_data.columns.values)
        # print(loan_data.loc[0])
        # loan_data.dropna()
        # loan_data.info()
        # loan_data.astype({"loan_amount": float})
        # print(loan_data.term.value_counts())
        loan_data['term'] = loan_data['term'].str[0:2]
        # loan_data.dropna()
        # print(loan_data.term.value_counts())
        loan_data['term'] = pd.to_numeric(loan_data['term'], downcast="integer")
        # loan_data.info()
        pd.options.display.float_format = '{:.2f}'.format
        # print(loan_data.shape)
        # print(loan_data.isna())
        a = loan_data.isna()
        for i in a:
            print(a[i].value_counts(sort=False))
        # print(loan_data.std())
        # print(loan_data.mths_since_last_major_derog.value_counts())
        # print(loan_data)
        return loan_data
    
    pass

DataTransform().correct_field_data_types()