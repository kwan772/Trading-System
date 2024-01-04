import pprint
from datetime import datetime, timedelta

import pytz
from backtesting.searcher import Searcher


class RangeSearcher(Searcher):
    def __init__(self, stats):
        super().__init__(stats)

    def search(self, symbol, data):
        # Assuming your current timezone is 'Pacific/Auckland'
        # and you want to convert to 'America/New_York'
        self.status[symbol.symbol] = self.analyze_data(data)

    from datetime import datetime, timedelta
    import pytz

    def get_session_range(self, data, start_time, end_time):
        """Calculate the high-low range for a given session"""
        session_data = [d for d in data if start_time <= d.datetime.time() <= end_time and end_time >= d.datetime.time()]
        if not session_data:
            return 0
        highs = [d.high for d in session_data if d.high is not None]
        lows = [d.low for d in session_data if d.low is not None]
        high = max(highs)
        low = min(lows)
        return (high - low) / low if highs and lows else 0

    def get_session_high(self, data, start_time, end_time):
        """Calculate the high-low range for a given session"""
        session_data = [d for d in data if start_time <= d.datetime.time() <= end_time and end_time >= d.datetime.time()]
        if not session_data:
            return 0
        highs = [d.high for d in session_data if d.high is not None]
        high = max(highs)
        return high

    def analyze_data(self, historical_prices):
        et_tz = pytz.timezone('America/New_York')
        results = {}
        # Group data by date
        sorted_data = sorted(historical_prices, key=lambda x: x.datetime)
        grouped_data = {}
        for d in sorted_data:
            converted_time = self.convert_timezone(d.datetime, 'UTC', 'America/New_York')
            d.datetime = converted_time
            if 9 <= d.datetime.hour <= 16:
                if 9 != d.datetime.hour or d.datetime.minute >= 30:
                    date_key = d.datetime.date().strftime("%Y-%m-%d")
                    grouped_data.setdefault(date_key, []).append(d)


        total = 0.0
        count = 1
        total_next_day_range_morning = 0
        next_day_count_morning = 0
        total_next_day_range_afternoon = 0
        next_day_count_afternoon = 0

        total_profit_morning_first = 0
        total_profit_afternoon_first = 0
        profit_count_morning_first = 1
        profit_count_afternoon_first = 1
        total_profit_morning_second = 0
        total_profit_afternoon_second = 0
        profit_count_morning_second = 1
        profit_count_afternoon_second = 1
        total_profit_afternoon_avg = 0
        profit_count_morning_avg = 1

        for date, data in grouped_data.items():
            date = datetime.strptime(date,"%Y-%m-%d")
            # Define session times
            morning_start = datetime.combine(date, datetime.strptime("09:30", "%H:%M").time())
            morning_end = datetime.combine(date, datetime.strptime("12:00", "%H:%M").time())
            afternoon_start = morning_end
            afternoon_end = datetime.combine(date, datetime.strptime("16:00", "%H:%M").time())

            # Calculate ranges
            morning_range = self.get_session_range(data, morning_start.time(), morning_end.time())
            afternoon_range = self.get_session_range(data, afternoon_start.time(), afternoon_end.time())

            # Check ratio
            if morning_range == 0:
                continue
            if afternoon_range == 0:
                continue
            total += morning_range + afternoon_range
            count += 2
            today_close = data[-1].close if data[-1].close is not None else data[-1].open
            # print(data[-1])
            # print(data)

            next_day = date + timedelta(days=1)
            next_day = next_day.strftime("%Y-%m-%d")

            if next_day in grouped_data:
                next_day_data = grouped_data[next_day]
                total_profit_afternoon_avg += (self.get_session_high(next_day_data, morning_start.time(), afternoon_end.time()) - today_close) / today_close
                profit_count_morning_avg += 1

            if morning_range / afternoon_range > 2:
                if next_day in grouped_data:
                    next_day_data = grouped_data[next_day]
                    next_day_morning_range = self.get_session_range(next_day_data, morning_start.time(), morning_end.time())
                    next_day_afternoon_range = self.get_session_range(next_day_data, afternoon_start.time(),
                                                                 afternoon_end.time())
                    next_day_morning_high = self.get_session_high(next_day_data, morning_start.time(),
                                                                    morning_end.time())
                    next_day_afternoon_high = self.get_session_high(next_day_data, afternoon_start.time(),
                                                                      afternoon_end.time())
                    if next_day_morning_range == 0:
                        continue
                    if next_day_afternoon_range == 0:
                        continue

                    if next_day_morning_high is None or next_day_afternoon_high is None:
                        continue

                    total_next_day_range_morning += next_day_morning_range + next_day_afternoon_range
                    next_day_count_morning += 2

                    total_profit_morning_first += (next_day_morning_high - today_close) / today_close
                    profit_count_morning_first += 1
                    total_profit_afternoon_first += (next_day_afternoon_high - today_close) / today_close
                    profit_count_afternoon_first += 1

            elif afternoon_range / morning_range > 2:
                if next_day in grouped_data:
                    next_day_data = grouped_data[next_day]
                    next_day_morning_range = self.get_session_range(next_day_data, morning_start.time(),
                                                                    morning_end.time())
                    next_day_afternoon_range = self.get_session_range(next_day_data, afternoon_start.time(),
                                                                      afternoon_end.time())
                    next_day_morning_high = self.get_session_high(next_day_data, morning_start.time(),
                                                                  morning_end.time())
                    next_day_afternoon_high = self.get_session_high(next_day_data, afternoon_start.time(),
                                                                    afternoon_end.time())
                    if next_day_morning_range == 0:
                        continue
                    if next_day_afternoon_range == 0:
                        continue

                    if next_day_morning_high is None or next_day_afternoon_high is None:
                        continue

                    total_next_day_range_afternoon += next_day_morning_range + next_day_afternoon_range
                    next_day_count_afternoon += 2
                    total_profit_morning_second += (next_day_morning_high - today_close) / today_close
                    profit_count_morning_second += 1
                    total_profit_afternoon_second += (next_day_afternoon_high - today_close) / today_close
                    profit_count_afternoon_second += 1

        if next_day_count_afternoon == 0:
            next_day_count_afternoon = 1
        if next_day_count_morning == 0:
            next_day_count_morning = 1

        return {"average":total/count,
                "next_day_average":{"morning":total_next_day_range_morning/next_day_count_morning,
                                    "afternoon":total_next_day_range_afternoon/next_day_count_afternoon},
                "next_day_profit":{"morning":{"first":total_profit_morning_first/profit_count_morning_first,
                                                "second":total_profit_morning_second/profit_count_morning_second},
                                    "afternoon":{"first":total_profit_afternoon_first/profit_count_afternoon_first,
                                                "second":total_profit_afternoon_second/profit_count_afternoon_second,
                                                 "avg":total_profit_afternoon_avg/profit_count_morning_avg}}
                }

    def convert_timezone(self, dt, from_zone, to_zone):
        from_tz = pytz.timezone(from_zone)
        to_tz = pytz.timezone(to_zone)
        return dt.replace(tzinfo=from_tz).astimezone(to_tz)
