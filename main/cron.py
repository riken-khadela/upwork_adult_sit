def my_cron_job():
    # your functionality goes here
    import datetime
    print(datetime.datetime.now())

    file1 = open("etc/z.txt", "a")  # append mode
    file1.write("Today \n")
    file1.close()