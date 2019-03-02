import logging
import instance

FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(FORMAT)
    logger.addHandler(handler)

    return logger

def transform_path(instance, starting_x, starting_y, path: list):

    if(starting_x == instance.x_min and starting_y == instance.x_min):
        transformed_path = path
    elif(starting_x == instance.x_max and starting_y == instance.y_max):
         transformed_path = path.reverse()
    elif(starting_x == instance.x_max and starting_y == instance.y_min):
         transformed_path = [(x,-y) for x,y in path]
    else:
         transformed_path = [(-x,y) for x,y in path]
    
    translated_path = [(x + instance.x_min, y + instance.y_min) for (x,y) in transformed_path]

    return translated_path
