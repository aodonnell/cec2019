import math

#fixme
import time

def clip_coord(x, y, max_x, max_y):
    """
    Clip coordinate between 0 and a set maximum. return a tuple containing the coord

    :param x:
    :param y:
    :param max_x:
    :param max_y:
    :return:
    """

    x = max(0, min(x, max_x - 1))
    y = max(0, min(y, max_y - 1))
    return x, y


def get_scan_path(size_x: int, size_y: int, scan_w):
    """
    Get ideal scan path coordinates

    :param size_x:
    :param size_y:
    :param scan_w:
    :return:
    """
    path = []

    curr_x = 0
    curr_y = 0

    # always start at top
    path.append((curr_x, curr_y))

    half_w = math.ceil(scan_w / 2)

    stride_x = scan_w + 1

    stride_y = -scan_w

    # from top left until we are completely out of bounds 
    # (last scan would ideally be the bottom right corner)
    while True:  

        # time.sleep(0.5)


        # if we're out of bounds already, go down our scan width +1 and our scan width over to the right.
        x_out = (curr_x >= size_x + scan_w or curr_x < 0 - scan_w)
        y_out = (curr_y >= size_y + scan_w or curr_y < 0 - scan_w)

        if x_out and y_out:
            break

        if x_out or y_out:

            # reverse x and y stride direction.
            stride_x *= -1
            stride_y *= -1

            if curr_x < 0 - scan_w:
                curr_y += scan_w + 1
                curr_x += scan_w
            elif curr_x >= size_x + scan_w:
                curr_y -= 2*scan_w + 1
                curr_x += scan_w
            elif curr_y < 0 - scan_w:
                curr_y -= scan_w
                curr_x += 2*scan_w + 1
            else:
                curr_y += scan_w
                curr_x += scan_w +1

            x_out = (curr_x >= size_x + scan_w or curr_x < 0 - scan_w)
            y_out = (curr_y >= size_y + scan_w or curr_y < 0 - scan_w)

            while(x_out or y_out):

                curr_x += stride_x
                curr_y += stride_y
                print(curr_x, curr_y)
                x_out = (curr_x >= size_x + scan_w or curr_x < 0 - scan_w)
                y_out = (curr_y >= size_y + scan_w or curr_y < 0 - scan_w)
        
        else:
            curr_x += stride_x
            curr_y += stride_y
            print(curr_x, curr_y)


        path.append(clip_coord(curr_x, curr_y, size_x, size_y))

    return path

if __name__ == '__main__':
    print(get_scan_path(10, 17, 1))