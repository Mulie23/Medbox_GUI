import vlc
def play_alarm():
    global alarm
    alarm = vlc.MediaPlayer('noti1.mp3')
    alarm.play()
    # sounds alarm 
    return True

def stop_alarm():
    alarm.stop()
    return True

play_alarm()