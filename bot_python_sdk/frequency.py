from enum import Enum


class Frequency(Enum):
    ALWAYS = 'always'
    YEARLY = 'yearly'
    HALF_YEARLY = 'half-yearly'
    MONTHLY = 'monthly'
    WEEKLY = 'weekly'
    DAILY = 'daily'
    HOURLY = 'hourly'
    MINUTELY = 'minutely'

    @staticmethod
    def is_valid(frequency):
        return frequency in FrequenciesInSeconds.keys()


FrequenciesInSeconds = {
    Frequency.ALWAYS.value: 0,
    Frequency.YEARLY.value: 31536000,  # Based on 365 days
    Frequency.HALF_YEARLY.value: 15768000,  # Half of yearly
    Frequency.MONTHLY.value: 2419200,  # Based on 28 days
    Frequency.WEEKLY.value: 604800,
    Frequency.DAILY.value: 86400,
    Frequency.HOURLY.value: 3600,
    Frequency.MINUTELY.value: 60
}
