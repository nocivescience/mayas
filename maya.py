from manim import *
class FirstScene(ZoomedScene):
    CONFIG={
        "plane_config":{
            "x_range":[-3,3,.5],
            "y_range":[-3,3,.5],
        },
        "complex_homotopy":lambda z,t:z**(1+t),
        "kwargs":{
            "run_time":2,
            "rate_func":smooth,
        },
        "num_anchors_to_add_per_line":20,
        "zoom_factor":0.05
    }
    def construct(self):
        plane=self.get_plane()[0]
        dots=self.get_dots(plane)
        self.edit_plane(plane)
        self.play(Create(plane))
        self.wait()
    def get_plane(self):
        top_plane=NumberPlane(**self.CONFIG['plane_config'])
        bottom_plane=top_plane.copy()
        return VGroup(top_plane,bottom_plane).arrange(DOWN).set_height(
            config['frame_height']
        )
    def edit_plane(self,plane):
        plane.set_stroke(YELLOW,width=0.5)
        self.add_foreground_mobject(plane)
    def get_dots(self,plane):
        dots=VGroup(*[
            Dot().move_to(
                plane.number_to_point(2,5)
            )
        ])
        return dots