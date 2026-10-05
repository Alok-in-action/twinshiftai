from manim import *

class DigitalTwinPresentation(Scene):
    def construct(self):
        # Title Slide
        title = Text("Baghewala Digital Twin", font_size=60, color=BLUE)
        subtitle = Text("Well-to-Surface Optimization", font_size=40)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(subtitle))

        # Expected Outcome
        outcome_title = Text("Expected Outcome", font_size=48, color=YELLOW)
        outcome_title.to_edge(UP)
        
        outcome_text = Text(
            "An AI-enabled Digital Twin\n"
            "integrating reservoir, wellbore,\n"
            "and surface production systems\n"
            "for real-time monitoring and optimization.",
            font_size=32,
            t2c={"Digital Twin": BLUE, "optimization": GREEN}
        )
        
        self.play(Write(outcome_title))
        self.play(FadeIn(outcome_text, shift=DOWN))
        self.wait(3)
        self.play(FadeOut(outcome_text))

        # The Solution Should
        solution_bullets = VGroup(
            Text("• Optimize CSS cycle parameters", font_size=28),
            Text("• Predict thermal & production performance", font_size=28),
            Text("• Continuously optimize SRP (SPM/stroke)", font_size=28),
            Text("• Detect rod floating & minimize impact", font_size=28),
            Text("• Improve pump efficiency & reliability", font_size=28),
            Text("• Optimize energy & steam consumption", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        solution_bullets.next_to(outcome_title, DOWN, buff=1.0)
        
        self.play(FadeOut(outcome_title))
        sol_title = Text("The Solution Should:", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(sol_title))
        
        for bullet in solution_bullets:
            self.play(FadeIn(bullet, shift=RIGHT), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(solution_bullets), FadeOut(sol_title))

        # Expected Benefits
        benefits_title = Text("Expected Benefits", font_size=48, color=YELLOW).to_edge(UP)
        
        benefits_bullets = VGroup(
            Text("✔️ Increased oil production & recovery", font_size=28, color=GREEN),
            Text("✔️ Reduced Steam-Oil Ratio (SOR)", font_size=28, color=GREEN),
            Text("✔️ Lower energy consumption per bbl", font_size=28, color=GREEN),
            Text("✔️ Reduced rod failures & pump unsetting", font_size=28, color=GREEN),
            Text("✔️ Improved equipment life & reliability", font_size=28, color=GREEN),
            Text("✔️ Data-driven predictive decisions", font_size=28, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        benefits_bullets.next_to(benefits_title, DOWN, buff=1.0)
        
        self.play(Write(benefits_title))
        self.play(Write(benefits_bullets), run_time=2.0)
        self.wait(3)
        self.play(FadeOut(benefits_bullets), FadeOut(benefits_title))

        # Data Availability
        data_title = Text("Data Architecture", font_size=48, color=YELLOW).to_edge(UP)
        
        data_text = Text(
            "Leveraging historical & real-time data:\n"
            "• Production & CSS cycle records\n"
            "• Steam injection & VFD parameters\n"
            "• Rod failure history & fluid properties",
            font_size=32
        )
        
        self.play(Write(data_title))
        self.play(FadeIn(data_text))
        self.wait(3)
        
        # Finale
        self.play(FadeOut(data_text), FadeOut(data_title))
        finale = Text("Baghewala Digital Twin", font_size=60, color=BLUE)
        self.play(Write(finale))
        self.wait(2)
