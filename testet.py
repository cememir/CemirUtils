from cemirutils import CemirUtils

utils = CemirUtils(None)

print(utils.days_between_dates("2024-05-01", "2024-05-25"))  # 24

print(utils.hours_minutes_seconds_between_times("08:30:00", "15:45:30"))  # (7, 15, 30)

print(utils.time_until_date("2024-05-27 23:59:59"))  # Kalan gün, saat, dakika, saniye

print(utils.add_days_and_format("2024-05-01", 30))  # "2024-05-31 (Cuma)"

print(utils.is_weekend("2024-05-25"))  # True

print(utils.is_leap_year(2024))  # True

print(utils.days_in_month(2024, 2))  # 29

print(utils.next_weekday("2024-05-25", 0))  # 2024-05-27

print(utils.time_since("2022-01-01 00:00:00"))  # (2, 4, 24, 14, 30, 15)

print(utils.business_days_between_dates("2024-05-01", "2024-05-25"))  # 17
