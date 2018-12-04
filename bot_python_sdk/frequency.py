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
    Frequency.ALWAYS: 0,
    Frequency.YEARLY: 31536000,  # Based on 365 days
    Frequency.HALF_YEARLY: 15768000,  # Half of yearly
    Frequency.MONTHLY: 2419200,  # Based on 28 days
    Frequency.WEEKLY: 604800,
    Frequency.DAILY: 86400,
    Frequency.HOURLY: 3600,
    Frequency.MINUTELY: 60
}
