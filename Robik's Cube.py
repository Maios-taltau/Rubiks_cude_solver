import cv2
import numpy as np
import kociemba as Cube
import time
import colorama
import serial

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED
MAGENTA = colorama.Fore.MAGENTA
colorama.init()

print(rf"{RED}                            _______    _________    __      ___      ___   ________    ________         ",
      end='\n')
print(rf"{GREEN}                           |  _____|  |   ___   |  |  |     \  \    /  /  |  ______|  |  _____ |    ")
print(rf"{GREEN}                           | |_____   |  |   |  |  |  |      \  \  /  /   | |____     |  ______|    ")
print(rf"{GREEN}                           |_____  |  |  |   |  |  |  |       \  \/  /    |  ____|    |   \  \        ")
print(rf"{GREEN}                            _____| |  |  |___|  |  |  |____    \    /     | |______   |  | \  \       ")
print(rf"{RED}                           |_______|  |_________|  |_______|    \__/      |________|  |__|  \__\      ")

time.sleep(2)
print("")
print("")
print(
    f"{MAGENTA}Please refer preview window for which side you have scanned and which color should be in centre on each side. ")

state = {
    'up': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'right': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'front': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'down': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'left': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'back': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ]
}

sign_conv = {
    'green': 'F',
    'white': 'U',
    'blue': 'B',
    'red': 'R',
    'orange': 'L',
    'yellow': 'D'
}

color = {
    'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'white': (255, 255, 255),
    'yellow': (0, 255, 255)
}

stickers = {
    'main': [
        [200, 120], [300, 120], [400, 120],
        [200, 220], [300, 220], [400, 220],
        [200, 320], [300, 320], [400, 320]
    ],
    'current': [
        [20, 20], [54, 20], [88, 20],
        [20, 54], [54, 54], [88, 54],
        [20, 88], [54, 88], [88, 88]
    ],
    'preview': [
        [20, 130], [54, 130], [88, 130],
        [20, 164], [54, 164], [88, 164],
        [20, 198], [54, 198], [88, 198]
    ],
    'left': [
        [50, 280], [94, 280], [138, 280],
        [50, 324], [94, 324], [138, 324],
        [50, 368], [94, 368], [138, 368]
    ],
    'front': [
        [188, 280], [232, 280], [276, 280],
        [188, 324], [232, 324], [276, 324],
        [188, 368], [232, 368], [276, 368]
    ],
    'right': [
        [326, 280], [370, 280], [414, 280],
        [326, 324], [370, 324], [414, 324],
        [326, 368], [370, 368], [414, 368]
    ],
    'up': [
        [188, 128], [232, 128], [276, 128],
        [188, 172], [232, 172], [276, 172],
        [188, 216], [232, 216], [276, 216]
    ],
    'down': [
        [188, 434], [232, 434], [276, 434],
        [188, 478], [232, 478], [276, 478],
        [188, 522], [232, 522], [276, 522]
    ],
    'back': [
        [464, 280], [508, 280], [552, 280],
        [464, 324], [508, 324], [552, 324],
        [464, 368], [508, 368], [552, 368]
    ],
}

font = cv2.FONT_HERSHEY_SIMPLEX
textPoints = {
    'up': [['U', 242, 202], ['W', (255, 255, 255), 260, 208]],
    'right': [['R', 380, 354], ['R', (0, 0, 255), 398, 360]],
    'front': [['F', 242, 354], ['G', (0, 255, 0), 260, 360]],
    'down': [['D', 242, 508], ['Y', (0, 255, 255), 260, 514]],
    'left': [['L', 104, 354], ['O', (0, 165, 255), 122, 360]],
    'back': [['B', 518, 354], ['B', (255, 0, 0), 536, 360]],
}

check_state = []
solution = []
solved = False

cap = cv2.VideoCapture(0)
#กำหนดชื่อ
cv2.namedWindow('frame')

def solve(state):
    raw = ''
    for i in state:
        for j in state[i]:
            raw += sign_conv[j]
    print("answer:", Cube.solve(raw))
    #solve() returns the solution as a string
    return Cube.solve(raw)


#HSV เป็นสีที่เกิดจากการผสมกันของ Hue (ค่าสี) , Saturation (ค่าความอิ่มตัวสี) และ Value (ค่าความสว่างของแสง)
def color_detect(h, s, v):
    #print(h, s, v)
    if h > 170 and h < 190 and s > 140 and s < 210 and v > 90 and v < 140:
        return 'red'
    elif h > 0 and h < 20 and s > 120 and s < 200 and v > 120 and v < 170:
        return 'orange'
    elif h > 20 and h < 45 and s > 120 and s < 170 and v > 120 and v < 170:
        return 'yellow'
    elif h > 70 and h < 90 and s > 150 and s < 210 and v > 80 and v < 120:
        return 'green'
    elif h > 90 and h < 120 and s > 150 and s < 210 and v > 120 and v < 180:
        return 'blue'
    elif h > 60 and h < 110 and s > 0 and s < 30 and v > 130 and v < 190:
        return 'white'

    return 'white'

#กรอบตรวจจับสี
def draw_stickers(frame, stickers, name):
    for x, y in stickers[name]:
        #สี่เหลียม (ภาพ, มุมบนซ้าย (x,y), มุมล่างซ้าน (x,y),  สี BRG, ความหนา)
        cv2.rectangle(frame, (x, y), (x + 30, y + 30), (255, 255, 255), 2)


#หน้าpreview
def draw_preview_stickers(frame, stickers):
    stick = ['front', 'back', 'left', 'right', 'up', 'down']
    for name in stick:
        for x, y in stickers[name]:
            cv2.rectangle(frame, (x, y), (x + 40, y + 40), (255, 255, 255), 2)


def texton_preview_stickers(frame, stickers):
    stick = ['front', 'back', 'left', 'right', 'up', 'down']
    for name in stick:
        for x, y in stickers[name]:
            sym, x1, y1 = textPoints[name][0][0], textPoints[name][0][1], textPoints[name][0][2]
            # putText(ภาพ, ข้อความ, พิกัดที่จะแสดง (x, y), font, ขนาดข้อความ, สี, ความหนา)
            cv2.putText(preview, sym, (x1, y1), font, 1, (0, 0, 0), 1)
            sym, col, x1, y1 = textPoints[name][1][0], textPoints[name][1][1], textPoints[name][1][2], \
            textPoints[name][1][3]
            # putText(ภาพ, ข้อความ, พิกัดที่จะแสดง (x, y), font, ขนาดข้อความ, สี, ความหนา)
            cv2.putText(preview, sym, (x1, y1), font, 0.5, col, 2)


#side = state, frame = preview
#ใส่สีที่ detect ได้ใน preview
def fill_stickers(frame, stickers, sides):
    for side, colors in sides.items():
        num = 0
        for x, y in stickers[side]:
            cv2.rectangle(frame, (x, y), (x + 40, y + 40), color[colors[num]], -1)
            num += 1


if __name__ == '__main__':

    preview = np.zeros((700, 700, 3), np.uint8)

    while True:
        hsv = []
        current_state = []
        ret, img = cap.read()
        #เปลี่ยนสีวิดิโอ
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #สร้าง matrix
        mask = np.zeros(frame.shape, dtype=np.uint8)

        #กรอบ detect
        draw_stickers(img, stickers, 'main')
        #กรอบ current
        draw_stickers(img, stickers, 'current')
        #วาดหน้า preview
        draw_preview_stickers(preview, stickers)
        #ใส่สีที่ detect ได้ใน preview
        fill_stickers(preview, stickers, state)
        #ใส่ข้อความหน้า preview
        texton_preview_stickers(preview, stickers)

        #เก็บค่า hsv จากกรอบ detect
        for i in range(9):
            hsv.append(frame[stickers['main'][i][1] + 10][stickers['main'][i][0] + 10])

        a = 0
        #ใส่สีลงในกรอบ current
        for x, y in stickers['current']:
            color_name = color_detect(hsv[a][0], hsv[a][1], hsv[a][2])
            cv2.rectangle(img, (x, y), (x + 30, y + 30), color[color_name], -1)
            a += 1
            #เก็บค่าสีที่ detect ได้
            current_state.append(color_name)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k == ord('u'):
            state['up'] = current_state
            check_state.append('u')
        elif k == ord('r'):
            check_state.append('r')
            state['right'] = current_state
        elif k == ord('l'):
            check_state.append('l')
            state['left'] = current_state
        elif k == ord('d'):
            check_state.append('d')
            state['down'] = current_state
        elif k == ord('f'):
            check_state.append('f')
            state['front'] = current_state
        elif k == ord('b'):
            check_state.append('b')
            state['back'] = current_state
        elif k == ord('\r'):
            if len(set(check_state)) == 6:
                #ตรวจความผิด
                try:
                    solved = solve(state)
                #ถ้าผิดจะทำ
                except:
                    print(
                        "error in side detection ,you may do not follow sequence or some color not detected well.Try again")
            else:
                print("all side are not scanned check other window for finding which left to be scanned?")
                print("left to scan:", 6 - len(set(check_state)))
        cv2.imshow('preview', preview)
        cv2.imshow('frame', img[0:500, 0:500])

    cv2.destroyAllWindows()