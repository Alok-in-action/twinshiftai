from manim import *
import random
import math

# Render Settings
config.pixel_width = 3840
config.pixel_height = 2160
config.frame_rate = 30
config.background_color = "#05080F"

# Palette
DEEP_BLUE = "#0B3D91"
CYAN = "#4DD0FF"
ORANGE = "#FF7A1A"
AMBER = "#FFB000"
ALERT_RED = "#FF2D2D"
OK_GREEN = "#2DFF7A"
TEXT_COLOR = "#E6F1FF"
BROWN = "#2B1A0F"

class WellDigitalTwin(MovingCameraScene):
    def construct(self):
        self.camera.frame.set_width(14.22) # Standard 16:9 frame width
        self.shot1()
        self.shot2()
        self.shot3()
        self.shot4()
        self.shot5()
        self.shot6()

    def glow(self, mob):
        """Return a VGroup of 3 copies of the mob to fake neon glow."""
        g = VGroup()
        for width, op in zip([12, 6, 2], [0.1, 0.25, 1.0]):
            c = mob.copy()
            if hasattr(c, "set_stroke"):
                c.set_stroke(width=width, opacity=op)
            g.add(c)
        return g

    def hud_label(self, txt, target_point, direction=RIGHT, buff=0.5):
        """A Text with a thin leader line and a small corner-bracket box."""
        lbl = Text(txt, font="Consolas", font_size=28, color=TEXT_COLOR)
        # Position label relative to target point
        if direction[0] > 0:
            lbl.next_to(target_point, direction, buff=buff)
        else:
            lbl.next_to(target_point, direction, buff=buff)
            
        line = Line(target_point, lbl.get_edge_center(-direction), stroke_width=1.5, color=CYAN)
        box = SurroundingRectangle(lbl, color=CYAN, stroke_width=1.5, buff=0.1)
        return VGroup(lbl, line, box)

    def _create_pumpjack(self):
        """Creates a simplified pumpjack VGroup."""
        base = Polygon([-1, 0, 0], [1, 0, 0], [0.5, 0.2, 0], [-0.5, 0.2, 0], color=DEEP_BLUE, fill_opacity=1)
        post = Line([0, 0.2, 0], [0, 1.5, 0], stroke_width=4, color=DEEP_BLUE)
        beam = Line([-1, 0, 0], [1, 0, 0], stroke_width=4, color=CYAN)
        beam.shift(UP * 1.5)
        horsehead = Circle(radius=0.2, color=DEEP_BLUE, fill_opacity=1).move_to(beam.get_end())
        pumpjack = VGroup(base, post, beam, horsehead)
        pumpjack.beam = beam
        pumpjack.horsehead = horsehead
        return pumpjack

    def shot1(self):
        # t=0s to 5s
        sky = Rectangle(width=16, height=9).set_fill(color=[ORANGE, DEEP_BLUE], opacity=1)
        sky.shift(UP*2)
        
        # Horizon
        horizon = Polygon([-8, -1, 0], [-4, 0, 0], [0, -1.5, 0], [5, 1, 0], [8, -0.5, 0], [8, -5, 0], [-8, -5, 0])
        horizon.set_fill(color="#020305", opacity=1).set_stroke(width=0)
        
        self.world = VGroup(sky, horizon)
        
        # Pumpjacks
        self.pumps = VGroup()
        for pos in [LEFT * 4, RIGHT * 2, RIGHT * 6]:
            pj = self._create_pumpjack().move_to(pos + DOWN * 0.5)
            self.pumps.add(pj)
            self.world.add(pj)
            
        # Add updater for pumpjacks
        self.pump_time = ValueTracker(0)
        def update_pumps(g):
            t = self.pump_time.get_value()
            for pj in self.pumps:
                angle = math.sin(t * 3) * 0.2
                pj.beam.set_angle(angle)
                pj.horsehead.move_to(pj.beam.get_end())
        self.pumps.add_updater(update_pumps)
        
        # Steam generator
        sg_base = Rectangle(width=1.5, height=0.8, color=ORANGE, fill_opacity=0.8)
        sg_stack = Rectangle(width=0.2, height=1, color=ORANGE, fill_opacity=0.8).next_to(sg_base, UP, buff=0)
        steam_gen = VGroup(sg_base, sg_stack).move_to(LEFT * 2 + DOWN * 0.5)
        self.world.add(steam_gen)
        
        # Steam particles
        steam_particles = VGroup(*[Circle(radius=0.1, color=WHITE, fill_opacity=0.5, stroke_width=0) for _ in range(15)])
        steam_particles.move_to(sg_stack.get_top())
        def update_steam(g, dt):
            for p in g:
                p.shift(UP * dt * random.uniform(1, 2) + RIGHT * dt * random.uniform(-0.5, 0.5))
                p.set_opacity(max(0, p.get_fill_opacity() - dt * 0.5))
                if p.get_fill_opacity() <= 0:
                    p.move_to(sg_stack.get_top())
                    p.set_opacity(random.uniform(0.3, 0.6))
        steam_particles.add_updater(update_steam)
        self.world.add(steam_particles)
        
        self.add(self.world)
        
        # Push in 0-3s
        self.play(
            self.camera.frame.animate.scale(0.7).move_to(LEFT*4 + DOWN*0.5),
            self.pump_time.animate.increment_value(3),
            run_time=3,
            rate_func=smooth
        )
        
        # 3-5s cyan wireframe of well draws in
        well_lines = VGroup(
            Line(LEFT*4 + DOWN*0.5, LEFT*4 + DOWN*4, color=CYAN),
            Line(LEFT*3.8 + DOWN*0.5, LEFT*3.8 + DOWN*4, color=CYAN)
        )
        well_glow = self.glow(well_lines)
        self.play(
            Create(well_glow),
            self.pump_time.animate.increment_value(2),
            run_time=2
        )
        
        self.world.add(well_glow)
        self.steam_particles = steam_particles

    def shot2(self):
        # t=5s to 10s
        # Transition down underground
        
        # Stop steam particles
        self.steam_particles.clear_updaters()
        
        # Add strata
        strata = Rectangle(width=16, height=10, color=BROWN, fill_opacity=1).move_to(DOWN*5)
        self.world.add_to_back(strata)
        
        self.play(
            self.camera.frame.animate.move_to(LEFT*4 + DOWN*4),
            self.pump_time.animate.increment_value(2),
            run_time=2
        )
        
        # Heat bubble
        heat_bubble = Ellipse(width=0.4, height=0.4, color=ORANGE, fill_opacity=0.5).move_to(LEFT*3.9 + DOWN*4)
        self.world.add(heat_bubble)
        bubble_tracker = ValueTracker(0.2)
        
        def update_bubble(b):
            r = bubble_tracker.get_value()
            b.set(width=r*2, height=r*2)
        heat_bubble.add_updater(update_bubble)
        
        # HUD
        temp_val = ValueTracker(60)
        temp_dec = Text("60", font="Consolas", font_size=28, color=ORANGE)
        def update_temp(d):
            new_text = Text(f"{int(temp_val.get_value())}", font="Consolas", font_size=28, color=ORANGE)
            new_text.move_to(d)
            d.become(new_text)
        temp_dec.add_updater(update_temp)
        
        lbl_temp = Text("Reservoir Temp: ", font="Consolas", font_size=28, color=TEXT_COLOR)
        vg_temp = VGroup(lbl_temp, temp_dec).arrange(RIGHT)
        
        target_point = LEFT*3.9 + DOWN*3
        direction = RIGHT*2
        vg_temp.next_to(target_point, direction, buff=0.5)
        line = Line(target_point, vg_temp.get_edge_center(-direction), stroke_width=1.5, color=CYAN)
        box = SurroundingRectangle(vg_temp, color=CYAN, stroke_width=1.5, buff=0.1)
        hud = VGroup(vg_temp, line, box)
        
        self.add(hud)
        
        self.play(
            bubble_tracker.animate.set_value(2.5),
            temp_val.animate.set_value(220),
            self.pump_time.animate.increment_value(3),
            run_time=3
        )
        
        # Cleanup shot2
        self.play(FadeOut(self.world), FadeOut(hud), run_time=0.5)
        self.camera.frame.move_to(ORIGIN).scale(1/0.7)
        self.clear()

    def shot3(self):
        # t=10s to 15s
        # Left half: wellbore + dyno
        tubing = Rectangle(width=0.5, height=6, color=CYAN, fill_opacity=0.1).move_to(LEFT * 4)
        plunger = Rectangle(width=0.4, height=0.5, color=ORANGE, fill_opacity=1)
        rod = Line(LEFT*4 + UP*3, plunger.get_top(), color=CYAN, stroke_width=4)
        
        stroke_tracker = ValueTracker(0)
        def update_plunger(p):
            t = stroke_tracker.get_value()
            y = math.sin(t * 3) * 2
            p.move_to(LEFT * 4 + UP * y)
            rod.put_start_and_end_on(LEFT*4 + UP*3, p.get_top())
        plunger.add_updater(update_plunger)
        
        self.add(tubing, plunger, rod)
        
        # Right half: Dyno Card
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=5, y_length=5).move_to(RIGHT * 3)
        ax_labels = ax.get_axis_labels(Text("Position", font_size=20), Text("Load", font_size=20))
        self.add(ax, ax_labels)
        
        distort = ValueTracker(0)
        def dyno_curve(t):
            # Parametric parallelogram that distorts
            d = distort.get_value()
            x = 5 + 4 * math.sin(t)
            # base load
            y_base = 5 + 3 * math.cos(t + math.pi/4)
            # if floating, downstroke load drops
            if math.cos(t) < 0: # downstroke roughly
                y = y_base * (1 - d * 0.8)
            else:
                y = y_base
            return ax.c2p(x, max(0, y))
            
        card = always_redraw(lambda: ParametricFunction(dyno_curve, t_range=[0, TAU], color=CYAN))
        self.add(card)
        
        alert_text = Text("Rod floating risk detected", font="Consolas", font_size=36, color=ALERT_RED).to_edge(UP)
        def update_alert(m):
            t = stroke_tracker.get_value()
            m.set_opacity(0.5 + 0.5 * math.sin(t * 10))
        alert_text.add_updater(update_alert)
        
        # 10 - 12s normal
        self.play(stroke_tracker.animate.increment_value(2), run_time=2)
        
        # 12 - 15s distort
        self.add(alert_text)
        self.play(
            stroke_tracker.animate.increment_value(3),
            distort.animate.set_value(1),
            run_time=3
        )
        
        self.shot3_objects = Group(tubing, plunger, rod, ax, ax_labels, card, alert_text)
        self.stroke_tracker = stroke_tracker
        self.distort = distort
        self.alert_text = alert_text

    def shot4(self):
        # t=15s to 21s
        # AI Recommendation
        
        # Neural net in center
        nn_group = VGroup()
        layers = [4, 6, 6, 3]
        dots = []
        for i, num_nodes in enumerate(layers):
            col = VGroup(*[Dot(color=CYAN) for _ in range(num_nodes)]).arrange(DOWN, buff=0.3)
            col.move_to(LEFT * 2 + RIGHT * i * 1.5)
            dots.append(col)
            nn_group.add(col)
            
        for i in range(len(layers)-1):
            for d1 in dots[i]:
                for d2 in dots[i+1]:
                    nn_group.add(Line(d1.get_center(), d2.get_center(), color=DEEP_BLUE, stroke_opacity=0.3))
                    
        nn_group.move_to(ORIGIN).scale(0.8)
        self.add(nn_group)
        
        # Output panel
        panel = RoundedRectangle(width=5, height=2, color=CYAN, fill_color="#05080F", fill_opacity=1).move_to(RIGHT*4 + DOWN*2)
        txt1 = Text("SPM 10 -> 8", font="Consolas", font_size=28, color=TEXT_COLOR).move_to(panel.get_center() + UP*0.3)
        txt2 = Text("VFD 42 -> 36 Hz", font="Consolas", font_size=28, color=TEXT_COLOR).move_to(panel.get_center() + DOWN*0.3)
        self.add(panel)
        
        self.play(
            Write(txt1), 
            Write(txt2), 
            self.stroke_tracker.animate.increment_value(2),
            run_time=2
        )
        
        # Morph back
        self.alert_text.clear_updaters()
        new_alert = Text("Stable", font="Consolas", font_size=36, color=OK_GREEN).to_edge(UP)
        
        self.play(
            self.stroke_tracker.animate.increment_value(4),
            self.distort.animate.set_value(0),
            Transform(self.alert_text, new_alert),
            run_time=4
        )
        
        self.play(FadeOut(self.shot3_objects), FadeOut(nn_group), FadeOut(panel), FadeOut(txt1), FadeOut(txt2), FadeOut(self.alert_text), run_time=0.5)

    def shot5(self):
        # t=21s to 26s
        # Dashboard split screen
        panels = VGroup()
        for i in range(4):
            r = RoundedRectangle(width=6, height=3, color=CYAN, fill_color="#05080F", fill_opacity=1)
            panels.add(r)
        panels.arrange_in_grid(rows=2, cols=2, buff=0.5)
        
        # Contents
        c1 = Text("Steam-Oil Ratio -12%", font="Consolas", font_size=32, color=OK_GREEN).move_to(panels[0])
        c2 = Text("Energy per barrel -10%", font="Consolas", font_size=32, color=OK_GREEN).move_to(panels[1])
        c3 = Text("Rod failures reduced ↓", font="Consolas", font_size=32, color=TEXT_COLOR).move_to(panels[2])
        c4 = Text("Oil production up ↑", font="Consolas", font_size=32, color=TEXT_COLOR).move_to(panels[3])
        
        self.play(
            LaggedStart(
                FadeIn(panels[0], c1, shift=UP),
                FadeIn(panels[1], c2, shift=UP),
                FadeIn(panels[2], c3, shift=UP),
                FadeIn(panels[3], c4, shift=UP),
                lag_ratio=0.2
            ),
            run_time=2
        )
        self.wait(2.5)
        
        self.panels_grp = VGroup(panels, c1, c2, c3, c4)
        self.play(FadeOut(self.panels_grp), run_time=0.5)

    def shot6(self):
        # t=26s to 30s
        # Closing
        # Reuse shot1
        self.world.set_opacity(0.2)
        self.add(self.world)
        self.play(
            self.camera.frame.animate.scale(1.5).move_to(ORIGIN),
            self.pump_time.animate.increment_value(2),
            run_time=2
        )
        
        title = Text("AI-Enabled Well-to-Surface Digital Twin", font="Consolas", font_size=48, color=CYAN)
        sub = Text("Predict. Optimize. Protect.", font="Consolas", font_size=36, color=ORANGE).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(sub, shift=UP), run_time=1)
        self.wait(0.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)

# ffmpeg -i media/videos/digital_twin/1080p60/WellDigitalTwin.mp4 -i score.mp3 -c:v copy -c:a aac -shortest out.mp4
