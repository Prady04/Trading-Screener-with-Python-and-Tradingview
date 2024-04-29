import datetime
import time

from colorama import Fore, init
import nifty50stockta as nta

if __name__ == "__main__":
    # Initialize colorama
    init()
    
      
        
    # Define market open and close times
    start_time_of_day = datetime.datetime.combine(datetime.date.today(), datetime.time(9, 15, 0))
    end_time_of_day = datetime.datetime.combine(datetime.date.today(), datetime.time(18, 30, 42))

    # Define target minutes for analysis
    target_minutes = [0,4,15,30,45]  # Minutes when analysis should run
    while True:
        now = datetime.datetime.now()

        if now < start_time_of_day:
            # Market has not yet opened
            print(Fore.YELLOW, 'Markets are yet to open...')
            time.sleep(60)  # Wait for 60 seconds before checking again

        elif now >= end_time_of_day + datetime.timedelta(minutes=1):
            # Market has closed
            print('Markets are closed...')
            break  # Exit the loop as the market has closed

        else:
            # Market is open, check if current minute is a target minute for analysis
            current_minute = now.minute
            next_target_minute = min(filter(lambda x: x > current_minute, target_minutes), default=None)

            if next_target_minute is None:
                # No future target minute found in the current hour, wait until the next hour
               time.sleep((60 - now.second))  # Wait until the start of the next minute
            
            else:
                # Calculate time to the next target minute
                time_to_next_interval = (next_target_minute - current_minute) * 60 - now.second
                print(Fore.YELLOW, f'Waiting for the next target minute... {int(time_to_next_interval)} seconds')

                if time_to_next_interval > 0:
                    print('#' * 55)
                    print(Fore.YELLOW, f'Waiting for the next target minute... {int(time_to_next_interval)} seconds')
                    time.sleep(time_to_next_interval)

                # Perform analysis at the target minute
                print('#' * 55)
                print(Fore.YELLOW, f"Algorithm starting at: { datetime.datetime.now().strftime('%d %b %Y %H:%M')} ")

                nta.get_data("15m")
                nta.get_data("1H")