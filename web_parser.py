#/usr/bin/python
dataframe = [
        {
            "current": {
                "count": 71,
                "metrics": {
                    "price": {
                        "sum": 45455.0
                    }
                }
            },
            "group": [
                "Womens Watch"
            ]
        },
        {
            "current": {
                "count": 81,
                "metrics": {
                    "price": {
                        "sum": 44374.0
                    }
                }
            },
            "group": [
                "Rings"
            ]
        },
        {
            "current": {
                "count": 84,
                "metrics": {
                    "price": {
                        "sum": 37312.0
                    }
                }
            },
            "group": [
                "Televisions"
            ]
        },
        {
            "current": {
                "count": 86,
                "metrics": {
                    "price": {
                        "sum": 36811.0
                    }
                }
            },
            "group": [
                "Loose Stones"
            ]
        },
        {
            "current": {
                "count": 84,
                "metrics": {
                    "price": {
                        "sum": 35429.0
                    }
                }
            },
            "group": [
                "Diamonds"
            ]
        },
        {
            "current": {
                "count": 74,
                "metrics": {
                    "price": {
                        "sum": 32365.0
                    }
                }
            },
            "group": [
                "Pendants"
            ]
        },
        {
            "current": {
                "count": 78,
                "metrics": {
                    "price": {
                        "sum": 31966.0
                    }
                }
            },
            "group": [
                "Gold"
            ]
        },
        {
            "current": {
                "count": 68,
                "metrics": {
                    "price": {
                        "sum": 31880.0
                    }
                }
            },
            "group": [
                "Bracelets"
            ]
        },
        {
            "current": {
                "count": 71,
                "metrics": {
                    "price": {
                        "sum": 29548.0
                    }
                }
            },
            "group": [
                "Mens Watch"
            ]
        },
        {
            "current": {
                "count": 84,
                "metrics": {
                    "price": {
                        "sum": 29527.0
                    }
                }
            },
            "group": [
                "Earrings"
            ]
        }
    ]

# "data":[["Monitors",147.0],["Sports-Apparel",63.0],["Wireless",719.0],["Mystery",24.0],["Sports",13.0],["Dresses",67.0],["Travel",8.0],["Televisions",2050.0],["Home Repair",7.0],["Memory",188.0]]}

dfParsed = []
columns = []
opKeys = ['sum','avg','max','min']
attrName = 'category'
columns.append(attrName)
for obj in dataframe:
    row = []
    for attr in obj['group']:
        row.append(attr)
    metrics = obj['current']['metrics']
    for field in  metrics:
        for op in opKeys:
            if metrics[field].get(op, False):
                row.append(metrics[field][op])
                metricName = '%s(%s)' % (field, op)
                if metricName not in columns:
                    columns.append(metricName)
    row.append(obj['current']['count'])
    dfParsed.append(row)
columns.append('count')
import pandas
df = pandas.DataFrame(dfParsed, columns=columns)
print (df)
