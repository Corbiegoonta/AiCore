from db_utils import RDSDatabaseConnector as rdbc
from data_info import DataFrameInfo as dfi
from data_handling import DataTransformation as dt

# df = rdbc().load_data_from_csv(r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\loan_payments.csv")

# print(df.columns[0])
# dfi().column_null_count(df)
# print(df.info())
# print(dt().drop_colums_with_significant_null_count(df, 35).info())
# dt().impute_columns_with_missing_data(dt().correct_field_data_types(dt().drop_colums_with_significant_null_count(df, 35)))

# a = "36 months"

# print(a[:2])

# a = 7.99
# a = a.lower()
# print(a)
# print(type(a))

# meal_to_be_removed = input("What meal do you want to remove?\n")
# with open("./meal_list.txt", "r") as file:
#     loaded_meal_list = file.read()
#     if meal_to_be_removed not in loaded_meal_list:
#         print("Sorry this meal is not in the meal list.")
#     else:
#         with open("./meal_list.txt", "w+") as files:
#             lines = files.readlines()
#             print(lines)
#             for line in lines:
#                 print(line)

# o = {"a": 1, "b": 2, "c": 3}
# print(o.items())

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(a[-1])