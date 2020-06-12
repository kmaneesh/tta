# Comtrade

## Usage limits

### Rate limit (guest):
1 request every second (per IP address or authenticated user).

### Rate limit (authenticated):
1 request every second (per IP address or authenticated user).

### Usage limit (guest):
100 requests per hour (per IP address or authenticated user).

### Usage limit (authenticated):
10,000 requests per hour (per IP address or authenticated user).

### Parameter combination limit:
* ps, r and p are limited to 5 codes each.
* Only one of the above codes may use the special ALL value in a given API call.
* Classification codes (cc) are limited to 20 items.
* ALL is always a valid classification code.


### Data availability request format
http://comtrade.un.org/api//refs/da/view?parameters


### Parameters
#### type trade data type (default = any) Valid values:
C Commodities (merchandise trade data)
S Services (trade in services data)

#### freq (default = any) data set frequency: Valid values:
A Annual
M Monthly

#### r (default = any) reporting area:
the area that reported the trade to UNSD.

#### ps time period (default = any):
Depending on freq, time period can take either YYYY or YYYYMM. For example:
Annual (YYYY): 2010
Monthly (YYYY or YYYYMM): Individual periods as 201001.

#### px classification (default = any):
Trade data classification scheme.