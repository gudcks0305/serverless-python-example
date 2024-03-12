import datetime
from dateutil.relativedelta import relativedelta
import json

data_list = {
    "2023-02-01": [1000, 2000],
    "2023-02-02": [1500, 2500],
    "2023-02-03": [1100, 2100]
}

def lambda_handler(event, context):
    try:
        print(event)
        params = event['queryStringParameters']

        Month = params.get('Month')
        Month_Total_data = {"list": [], "Month_Total_Discharge": 0, "Month_Total_Charge": 0}
        Month_Total_Discharge = 0
        Month_Total_Charge = 0

        year, month = Month.split('-')
        year = int(year)
        month = int(month)


        mon_date = datetime.date(year, month, 1)
        mon_next_date = mon_date + relativedelta(months=1)
        mon_last_day = mon_next_date - datetime.timedelta(days=1)
        Last_day = int(mon_last_day.day)

        for day_list in range(1, Last_day + 1):
            day_key = f"{Month}-{day_list:02d}"
            Log_data = data_list.get(day_key, [0, 0])

            Charge_value, Discharge_value = Log_data

            Month_Total_Discharge += Discharge_value
            Month_Total_Charge += Charge_value

            Month_val = {
                'Day': day_list,
                'Total_Discharge': Discharge_value * 1e-6,
                'Total_Charge': Charge_value * 1e-6
            }

            Month_Total_data['list'].append(Month_val)

        Month_Total_data['Month_Total_Discharge'] = Month_Total_Discharge * 1e-6
        Month_Total_data['Month_Total_Charge'] = Month_Total_Charge * 1e-6

        return {
            "statusCode": 200,
            "body": json.dumps(Month_Total_data),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }

if __name__ == "__main__":
    context = {}
    response = lambda_handler(event, context)
    print("Lambda Response:", response)

