from set_coordinates import ClickPoints 

class Get_Coordinates:
    def __init__(self, in_video_path, frame_size, area1_coordinates=None, area2_coordinates=None):
        self.in_video_path = in_video_path
        self.area1_coordinates = area1_coordinates
        self.area2_coordinates = area2_coordinates    
        self.frame_size = frame_size

    def get_coordinates(self, current_coordinates, other_coordinates, area):
        if not current_coordinates:
            click_points = ClickPoints(self.in_video_path, other_coordinates)
            current_coordinates = click_points.run(self.frame_size)

        if not current_coordinates:
            print(f"Area {area} No coordinates")
            return None

        if len(current_coordinates) < 4:
            print(f"Area {area} Incomplete")
            return None

        return current_coordinates
    