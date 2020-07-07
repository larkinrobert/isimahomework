import pandas as pd
import numpy as np
from io import StringIO
from pandas_schema import Column, Schema
from pandas_schema.validation import LeadingWhitespaceValidation, TrailingWhitespaceValidation, CustomElementValidation, CanConvertValidation, MatchesPatternValidation, InRangeValidation, InListValidation

null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
phone_validation = [MatchesPatternValidation(r'\(\d{3}\) \d{3}-\d{4}')]
#this regex isn't good enough, but I'm out of time.
email_validation = [MatchesPatternValidation(r'[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}')]

schema = Schema([
    Column('NAME', null_validation),
    Column('EMAIL', null_validation + email_validation),
    Column('PHONE', null_validation + phone_validation)
])

test_data = pd.read_csv('data/CorruptedDummyData.csv')

dupe_names = test_data[test_data.duplicated(subset="NAME", keep=False)].sort_values(by="NAME",axis=0, ascending=True, inplace=False)

print("DUPLICATE NAMES")
print(dupe_names)
print("#################")

missing_data_by_email = test_data.fillna("MISSING", inplace=False).sort_values(by="EMAIL")
missing_data_by_name = test_data.fillna("MISSING", inplace=False).sort_values(by="NAME")
print("#################")
print("ROWS MISSING 'NAME'")
print(missing_data_by_email.loc[missing_data_by_email['NAME'] == 'MISSING'])
print("#################")

print("ROWS MISSING 'EMAIL'")
print(missing_data_by_name.loc[missing_data_by_email['EMAIL'] == 'MISSING'])
print("#################")

print("ROWS MISSING 'PHONE'")
print(missing_data_by_name.loc[missing_data_by_email['PHONE'] == 'MISSING'])
print("#################")

print(test_data.info())

errors = schema.validate(test_data)

for error in errors:
    print(error)


