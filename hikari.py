# coding: utf-8
# 参考：「みんなのRaspberry Pi入門」リックテレコム 石井もルナ・江崎徳秀 著

# spi, time ライブラリをインポート
import spidev
import time
import RPi.GPIO as GPIO
from slack import SlackMessage 

ledflag = False
slackPost = SlackMessage()

GPIO.setmode(GPIO.BCM) 
led_channel = 4
GPIO.setup(led_channel, GPIO.OUT)
GPIO.output(led_channel, GPIO.HIGH)

# SpiDev オブジェクトのインスタンスを生成
spi = spidev.SpiDev()

# ポート0、デバイス0のSPI をオープン
spi.open(0, 0)

# 最大クロックスピードを1MHz に設定
spi.max_speed_hz=1000000

# 1 ワードあたり8ビットに設定
spi.bits_per_word=8

# ダミーデータを設定（1111 1111）
dummy = 0xff

# スタートビットを設定（0100 0111）
start = 0x47

# シングルエンドモードを設定 （0010 0000）
sgl = 0x20

# ch0 を選択（0000 0000）
ch0 = 0x00
# ch1 を選択（0001 0000）
ch1 = 0x10

# MSB ファーストモードを選択（0000 1000）
msbf = 0x08

# IC からデータを取得する関数を定義
def measure(ch):
    # SPI インターフェイスでデータの送受信を行う
    ad = spi.xfer2( [ (start + sgl + ch + msbf), dummy ] )
    #
    val = ((ad[0] & 0x03) << 8) + ad[1] 
    # 受信した2バイトのデータを10 ビットデータにまとめる
    voltage =  ( val * 3.3 ) / 1023
    # 結果を返す
    return val, voltage

# アナログデータを読み取る
def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out

# 例外を検出
try:
    # 無限ループ
    while 1:
        # 関数を呼び出してch0 のデータを取得
        ch0_val, ch0_voltage  = measure(ch0)
        # 関数を呼び出してch1 のデータを取得
        ch1_val, ch1_voltage  = measure(ch1)
        # 結果を表示
        #print  (' ch0 = {:4d}, {:2.2f}[V], ch1 = {:4d}, {:2.2f}[V]'.format(ch0_val, ch0_voltage, ch1_val, ch1_voltage))
        reading0 = analog_read(ch0)
        voltage0 = reading0 * 3.3 / 1024
        temp_c0 = voltage0 * 100 - 50
        print("Volts_ch0 V=%f\tTemp C_ch0=%f" % (voltage0, temp_c0))
        #print(reading0)
        reading = analog_read(ch1)
        voltage = reading * 3.3 / 1024
        temp_c = voltage * 100 - 50
        #print("Volts_ch1 V=%f\tTemp C_ch1=%f" % (voltage, temp_c))
        # 0.5 秒待つ
        
        if voltage0 == 0:
            #何もしない
            ledflag = ledflag
        elif voltage0 > 0.1 and ledflag == False:
        #GPIO.setmode(GPIO.BCM) 
        #GPIO.setup(led_channel, GPIO.OUT)

            GPIO.output(led_channel, True)
            ledflag = True
            slackPost.post()
        #time.sleep(2.0)
        elif voltage0 > 0.1 and ledflag == True:
            #何もしない
            ledflag = ledflag
        else:
            GPIO.output(led_channel, False)
            ledflag = False
        time.sleep(0.5)

# キーボード例外を検出
except KeyboardInterrupt:
    # 何も処理をしない
    GPIO.cleanup()
    pass

# SPI を開放
spi.close()