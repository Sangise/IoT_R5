import smbus #I2C通信を使うためのライブラリ(必要)
from time import sleep #sleepを使うためのライブラリ

def read_adt7410():
    
    #設定レジスタの書き換え　0x03 -> 0x00:13bit
    bus.write_byte_data(0x48, 0x03, 0x00)
    
    #温度レジスタの読み取り　0x00:温度上位レジスタ 0x01:温度下位レジスタ
    temp_most  = bus.read_byte_data(0x48,0x00)
    temp_least = bus.read_byte_data(0x48,0x01)
    
    #温度レジスタの上位と下位の結合。上位を8ビット左にずらして、下位ビットと連結
    temp_data = (temp_most<<8) | temp_least
    
    #下位3bitは要らない情報なので、全体を3bit右にずらして、有効な13bitのみ残す
    temp = (temp_data >> 3)
    
    #温度値が＋かーを13bit目に書かれているので、12bit右にずらして0か1かを確認する
    if (temp >> 12) == 0:  #13bit目が0(+)であれば
        temperature = temp * 0.0625 #分解能0.0625をかける
    elif (temp >> 12) == 1:#13bit目が1(-)であれば
        temp_minus  = temp - 8192 #負の補数対策
        temperature = temp_minus * 0.0625 #分解能0.0625をかける
    
    return temperature #値をメインに返す

#----main---#
bus = smbus.SMBus(1) #I2C(smbus)の設定

try:
    while True:
        inputValue = read_adt7410() #read_adt7410()を呼び出して温度値を取得
        print(inputValue)
        sleep(3)
        
except KeyboardInterrupt:
    print("END")