# vision.py by CoccaGuo at 2022/03/02 12:59
import configparser
import cv2
import numpy as np

stm_list = p_list = None
# read params for vision processing

cfg = configparser.ConfigParser()
cfg.read('settings.conf')
cf_rot = cfg.getfloat('ccd_location', 'rotation')
cf_top = cfg.getint('ccd_location', 'top')
cf_btm = cfg.getint('ccd_location', 'bottom')
cf_stm_left = cfg.getint('ccd_location', 'stm_left')
cf_stm_right = cfg.getint('ccd_location', 'stm_right')
cf_p_left = cfg.getint('ccd_location', 'prep_left')
cf_p_right = cfg.getint('ccd_location', 'prep_right')
cf_thres = cfg.getint('process', 'threshold')


# rotate image by degree
def rotate(image, degree):
    # rotate image by degree
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, degree, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def seven_blocked_test(img):
    # top
    # threshold ~ 0.25 - 0.3
    res = 0b0000_0000
    res = (res | (img[1:5, 5:18].sum()/(255*4*13) > 0.3)) << 1
    res = (res | (img[12:16, 5:14].sum()/(255*4*9) > 0.3)) << 1
    res = (res | (img[23:28, 3:14].sum()/(255*5*11) > 0.3)) << 1
    # left
    res = (res | (img[4:14, 3:8].sum()/(255*10*5) > 0.25)) << 1
    res = (res | (img[16:26, 1:6].sum()/(255*10*5) > 0.25)) << 1
    # right
    res = (res | (img[4:14,  14:20].sum()/(255*10*6) > 0.25)) << 1
    res =  res | (img[16:26,  12:18].sum()/(255*10*6) > 0.25)
    # top, mid, btm, left_up, left_down, right_up, right_down
    return res


def special_one_test(img):
    if img[1: 28, 7: 13].sum()/(255*5*11) > 0.30:
        return 1
    else: return "?"


def get_result_from_code(img, res):
    # 0: 101_1111, 95
    # 1: 000_0011, 3
    # 2: 111_0110, 118
    # 3: 111_0011, 115
    # 4: 010_1011, 43
    # 5: 111_1001, 121
    # 6: 111_1101, 125
    # 6': 011_1101, 61
    # 7: 100_0011, 67
    # 8: 111_1111, 127
    # 9: 111_1011, 123
    # 9', 110_1011, 107
    # -, 010-0000, 32
    code_ = {95: 0, 3:1, 118:2, 115:3, 43:4, 121:5, 125:6, 61:6, 67:7, 127:8, 123:9, 107:9}
    try: 
        return code_[res]
    except KeyError:
        return special_one_test(img)

# parse single item
def parse_item(img, left, right):
    area_img = img[cf_top:cf_btm, left:right]
    # convert the area_img to gray scale
    gray_img = cv2.cvtColor(area_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_img, (3, 3), 0)
    thres, dst = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
    dst = dst.astype(np.uint8)
    contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
    dst_color = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(dst_color, contours, -1, (0, 0, 255), 1)

    area_list = [cv2.contourArea(i) for i in contours]
    thres = np.average(area_list)/2

    def getArea(contour):
        xl, yl = [], []
        for c in contour:
            xl.append(c[0][0])
            yl.append(c[0][1])
        return np.min(xl), np.max(xl), np.min(yl), np.max(yl)

    size_chart = []
    for i in contours:
        if cv2.contourArea(i) < thres: continue
        xs, xm, ys, ym = getArea(i)
        size_chart.append([[xs, ys], [xm, ym]])

    size_chart = sorted(size_chart, key=lambda x: x[0][0])
    x_min = dst.shape[0]
    x_max = delta_y_max = 0
    for i in size_chart:
        x_min = min(i[0][1], x_min)
        x_max = max(i[1][1], x_max)
        dty = i[1][0] - i[0][0]
        delta_y_max = max(delta_y_max, dty)

    for i in size_chart:
        i[0][1] = x_min-1
        i[1][1] = x_max+1
        dty_ = delta_y_max - (i[1][0] - i[0][0])
        i[0][0] -= (dty_ - int(dty_/2-1))
        i[1][0] += int(dty_/2+1)

    x = 0
    sub_data_list = []
    for i in size_chart:
        x += 1
        sub_data = gray_img[i[0][1]: i[1][1], i[0][0]: i[1][0]]
        sub_data = cv2.resize(sub_data, (20, 28))
        sub_data_list.append(sub_data)


    x = 1
    result = []
    for img in sub_data_list:
        # GuassianBlur img
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        # set threshold value 40
        _, img = cv2.threshold(blurred, cf_thres, 255, cv2.THRESH_BINARY)
        # plot the threshold image
        x += 1
        code = seven_blocked_test(img)
        result.append(get_result_from_code(img, code))
    return result


def parse_pressure(data_list):
    if data_list[-1] == 0:
        return f"{data_list[0]}.{data_list[1]} e-10"
    return f"{data_list[0]}.{data_list[1]} e-{data_list[-1]}"

# process the picture
def process(img):
    image = rotate(img, cf_rot)
    stm_list = parse_item(image, cf_stm_left, cf_stm_right)
    p_list = parse_item(image, cf_p_left, cf_p_right)
    # process pressure
    p_prep = parse_pressure(p_list)
    p_stm = parse_pressure(stm_list)
    return p_stm, p_prep


