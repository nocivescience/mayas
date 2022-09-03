from manimlib.imports import *
class FirstExperience3(ComplexTransformationScene,ZoomedScene):
    CONFIG={
        "plane_config":{
            "x_line_frequency":0.5,
            "y_line_frequency":0.5
        },
        "complex_homotopy":lambda z,t:z**(1+t),
        "kwargs":{
            "run_time":2,
            "rate_func":smooth,
        },
        "num_anchors_to_add_per_line":20,
        "zoom_factor":0.05
    }
    def setup(self):
        ComplexTransformationScene.setup(self)
        ZoomedScene.setup(self)
    def construct(self):
        #self.edit_plane()
        #self.add_transforming()
        self.get_dots()
        self.getting_camera()
        self.get_homotopy()
    def get_plane(self):
        top_plane=NumberPlane(**self.plane_config)\
            .next_to(ORIGIN,UP,0.001)
        bottom_plane=top_plane.copy()
        bottom_plane.next_to(ORIGIN,DOWN,0.001)
        return VGroup(top_plane,bottom_plane)
    
    def edit_plane(self):
        self.background.set_stroke(GRAY,width=0.5)
        self.add_foreground_mobject(self.background.coordinate_labels)
    def add_transforming(self):
        plane=self.get_plane()
        self.add_transformable_mobjects(plane)
    def getting_camera(self):
        frame=self.zoomed_camera.frame
        point_mob=VectorizedPoint(
            self.background.number_to_point(
                complex(-3,1)
            )
        )
        frame.move_to(point_mob)
        tiny_plane=NumberPlane(
            x_radius=2,
            y_radius=2,
            color=BLUE_A
        )
        tiny_plane.replace(frame)
        #self.play(ShowCreation(self.get_plane()),**self.kwargs)
        self.activate_zooming(animate=True)
        self.play(ShowCreation(tiny_plane))
        self.play(VGroup(frame,tiny_plane).move_to,
            VectorizedPoint(self.background.number_to_point(complex(-1.5,0.8))),
            run_time=3,rate_func=smooth
                )
        self.play(
            VGroup(frame,tiny_plane).move_to,
            VectorizedPoint(self.background.number_to_point(self.complex_homotopy(complex(
                -1.5,0.8
            ),1))),path_arc=angle_of_vector(self.background.number_to_point(
                complex(-1.5,0.8))),
                run_time=3,rate_func=smooth
        )
    def get_dots(self):
        dots=VGroup(*[
            Dot().move_to(self.background.number_to_point(z)) for z in [
                1,complex(-1.5,0.8)
            ]
        ])
        self.dots=dots
        dot_groups=VGroup()
        for dot in dots:
            point=dot.get_center()
            z=self.background.point_to_number(point)
            z_out=self.complex_homotopy(z,1)
            point_out=self.background.number_to_point(z_out)
            dot_out=dot.copy()
            dot_out.move_to(point_out)
            s_angle=30*DEGREES
            if abs(z-1)<0.01:
                arrow=Arc(
                    start_angle=-90*DEGREES+s_angle,
                    angle=360*DEGREES-2*s_angle,
                    radius=0.17
                )
                arrow.add_tip(tip_length=0.15)
                arrow.pointwise_become_partial(arrow,0.05,1)
                arrow.next_to(dot,UP,0)
            else:
                arrow=Arrow(dot,dot_out,path_arc=angle_of_vector(point),buff=SMALL_BUFF)
            dot_group=VGroup(dot,arrow,dot_out)
            dot_groups.add(dot_group)
            dot.save_state()
            dot_group.anim=Succession(
                ApplyMethod(dot.restore),
                AnimationGroup(ShowCreation(arrow)),
                TransformFromCopy(dot,dot_out)
            )
        #for dot_group in dot_groups:
        #    self.play(dot_group.anim,**self.kwargs)
        self.play(*[m.anim for m in dot_groups])
        self.wait()
        self.dot_groups=dot_groups
    def get_homotopy(self):
        dot_groups=self.dot_groups
        self.play(ShowCreation(self.get_plane()))
        self.apply_complex_homotopy(self.complex_homotopy,
            added_anims=[Animation(dot_groups)]
                )
        self.wait(2)