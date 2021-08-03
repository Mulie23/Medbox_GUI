import vlc
def play_alarm():
    global alarm
    alarm = vlc.MediaPlayer('samsung_alarm.mp3')
    alarm.play()
    # sounds alarm 
    return True

def stop_alarm():
    alarm.stop()
    return True