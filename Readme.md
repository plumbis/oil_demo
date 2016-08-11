This demonstrates dynamic route changes based on the price of a stock.

The file /roles/leafs/files/stock_price.py provides the functionality.

Within the python file the following code drives the check
```

    TARGET_PRICE = 25.00

    # 32.93
    high_price = stock.get_historical(high_date, high_date)[0]["Close"]

    # 24.30
    low_price = stock.get_historical(low_date, low_date)[0]["Close"]
```
You can use `get_historical()` to pull a stock price from a point in time or `get_price()` for the current price.

In order to demonstrate the change a historic point in time is used.

First define the `TARGET_PRICE` value.
Next define `current_price` by whatever price lookup method you wish.

This assume eBGP is in use with unnumbered. When a change needs to be made a BGP AS path is appened or remoted based on the price change.

Leaf1 will adjust the ECMP path between spines to reach Leaf2. Executing the script with `python stock_price.py` in /home/vagrant will exectue the change.

