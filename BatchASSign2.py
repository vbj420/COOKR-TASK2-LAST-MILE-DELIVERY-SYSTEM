import pandas as pd
from datetime import datetime, timedelta

# Read Orders.csv
orders_df = pd.read_csv('Orders.csv')

# Initialize batch count
batch_count = 1

# Create an empty dictionary to store batches
batches = {}

# Function to convert time string to datetime object
def str_to_time(time_str):
    return datetime.strptime(time_str, '%H:%M')

# Function to check if two times are within 10 minutes of each other
def within_10_minutes(time1, time2):
    return abs((time1 - time2).total_seconds()) / 60 <= 10

# Loop through each order
while not orders_df.empty:
    # Get the first order
    first_order = orders_df.iloc[0]

    # Convert delivery time to datetime object
    first_order_time = str_to_time(first_order['Delivery Time'])

    # 1 . SAME KITCHEN SAME CUSTOMER SAME TIME
    # Filter orders based on the conditions
    same_kitchen_same_customer_same_time = orders_df[
        (orders_df['Kitchen ID'] == first_order['Kitchen ID']) &
        (orders_df['Customer Name'] == first_order['Customer Name']) &
        (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time)))
    ]

    #2. SAME CUSTOMER DIFF KITCH CLOSE SAME TIME
    same_customer_close_distance_same_time = orders_df[
        (orders_df['Customer Name'] == first_order['Customer Name']) &
        (orders_df['Distance from Kitchen'] <= 10) &
        (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time)))
    ]

    # 3. SAME KITCHEN DIFF CUSTOMER CLOSE SAME TIME
    different_customer_same_kitchen_same_time = orders_df[
        (orders_df['Kitchen ID'] == first_order['Kitchen ID']) &
        (orders_df['Distance from Kitchen'] <= 10) &
        (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time)))
    ]

    # 4. SAME CUST , DIFF KITCHEN , 2ND ON THE WAY 
    same_customer_different_kitchen_same_time = orders_df[
     (orders_df['Customer Name'] == first_order['Customer Name']) &
     (orders_df['Kitchen ID'] != first_order['Kitchen ID']) &
     (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time)))
    ]

    if not same_customer_different_kitchen_same_time.empty:
         if (first_order['Kitchen Location X'] == first_order['Customer Location X'] and
                 first_order['Kitchen Location Y'] <= first_order['Customer Location Y']):
             rule = 4
         elif (first_order['Kitchen Location Y'] == first_order['Customer Location Y'] and
               first_order['Kitchen Location X'] <= first_order['Customer Location X']):
             rule = 4
         else:
            same_customer_different_kitchen_same_time = pd.DataFrame()
    
    #5.
    different_customer_same_time = orders_df[
            (orders_df['Customer Name'] != first_order['Customer Name']) &
            (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time)))
        ]

    different_customer_same_kitchen_same_time = orders_df[
        (orders_df['Kitchen ID'] == first_order['Kitchen ID']) &
        (orders_df['Distance from Kitchen'] <= 10) &
        (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time))) &
        (orders_df['Customer Location X'] == first_order['Customer Location X']) &
        (orders_df['Customer Location Y'] <= first_order['Customer Location Y'])
    ]

    if not different_customer_same_kitchen_same_time.empty:
        rule = 5
    else:
        different_customer_same_kitchen_same_time = orders_df[
            (orders_df['Kitchen ID'] == first_order['Kitchen ID']) &
            (orders_df['Distance from Kitchen'] <= 10) &
            (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time)))
        ]

        if not different_customer_same_kitchen_same_time.empty:
            if (first_order['Customer Location X'] == first_order['Kitchen Location X'] and
                    first_order['Kitchen Location X'] == first_order['Customer Location X']):
                rule = 5
            elif (first_order['Customer Location Y'] == first_order['Kitchen Location Y'] and
                    first_order['Kitchen Location X'] == first_order['Customer Location X']):
                rule = 5
            else :
                different_customer_same_kitchen_same_time  = pd.DataFrame()
                
    different_customer_same_kitchen_same_time = orders_df[
        (orders_df['Kitchen ID'] == first_order['Kitchen ID']) &
        (orders_df['Customer Location X'] != first_order['Customer Location X']) &
        (orders_df['Customer Location Y'] != first_order['Customer Location Y']) &
        (orders_df['Delivery Time'].apply(lambda x: within_10_minutes(str_to_time(x), first_order_time)))
    ]

    if not different_customer_same_kitchen_same_time.empty:
        if (first_order['Customer Location X'] == first_order['Kitchen Location X'] and
                first_order['Customer Location Y'] < first_order['Kitchen Location Y']):
            rule = 6
        elif (first_order['Customer Location Y'] == first_order['Kitchen Location Y'] and
                first_order['Customer Location X'] < first_order['Kitchen Location X']):
            rule = 6
        else :
            different_customer_same_kitchen_same_time = pd.DataFrame()

    # Assign orders to batch
    batch_orders = pd.concat([same_kitchen_same_customer_same_time,
                              same_customer_close_distance_same_time,
                              different_customer_same_kitchen_same_time,
                              same_customer_different_kitchen_same_time,
                              different_customer_same_time,
                              different_customer_same_kitchen_same_time])

    # Store batch orders in batches dictionary
   # Store batch orders in batches dictionary
    for _, order in batch_orders.iterrows():
        rule = 0  # Default rule is 0, meaning no specific rule matched
        if order.name in same_kitchen_same_customer_same_time.index:
            rule = 1
        elif order.name in same_customer_close_distance_same_time.index:
            rule = 2
        elif order.name in different_customer_same_kitchen_same_time.index:
            rule = 3
        elif order.name in same_customer_different_kitchen_same_time.index:
            rule = 4
        elif order.name in different_customer_same_time.index:
            rule = 5
        elif order.name in different_customer_same_kitchen_same_time.index:
            rule = 6
    
        batches.setdefault(batch_count, []).append(
            [*order[['Customer Name', 'Kitchen ID', 'Food Name', 'Delivery Time']].tolist(), rule])

    # Remove batch orders from orders_df
    orders_df = orders_df.drop(batch_orders.index)

    # Increment batch count
    batch_count += 1

# Write batches to Batches.csv
with open('Batches.csv', 'w') as f:
    f.write('batchnum,custname,kitchenname,foodname,delivery time,rule\n')
    for batch_num, orders in batches.items():
        for order in orders:
            f.write(f"{batch_num},{order[0]},{order[1]},{order[2]},{order[3]},{order[4]}\n")
