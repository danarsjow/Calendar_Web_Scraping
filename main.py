import time as time
import sys as sys
from public_holiday_scrape import cleaned_df


def input_error():
    print('Invalid input!')
    sys.exit(0)

def stop_process():
    sys.exit(0)

# Main process
def project():
    while True:
        user_input = input('Silahkan input tanggal untuk diperiksa (format yyyy-mm-dd) : \n')
        cleaned_df['Tanggal'].to_string
        if user_input in cleaned_df['Tanggal'].to_string():
            print(user_input+' adalah hari libur')
            time.sleep(1)
        else: 
            print(user_input+' bukan hari libur')
        time.sleep(1)

        proceeed = input("Ingin terus memeriksa? (hanya jawab ya/tidak) :\n")
        if proceeed.lower() == 'tidak':
            stop_process()
        if proceeed.lower() == 'ya': 
            continue
        else: input_error()

if __name__ == "__main__":
    project()
        