"""
Tkinter GUI for the flashcard application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from models import Card, DeckMetadata
from datetime import datetime


class LoginScreen:
    """Login/user selection screen."""
    
    def __init__(self, root: tk.Tk, on_login: Callable[[str], None], 
                 existing_users: list[str]):
        self.root = root
        self.on_login = on_login
        self.existing_users = existing_users
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(self.frame, text="Japanese Flashcard App", 
                         font=('Arial', 24, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username entry
        ttk.Label(self.frame, text="Username:", font=('Arial', 12)).grid(
            row=1, column=0, sticky=tk.W, pady=10)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.frame, textvariable=self.username_var,
                                       font=('Arial', 12), width=20)
        self.username_entry.grid(row=1, column=1, pady=10)
        self.username_entry.focus()
        
        # Login button
        login_btn = ttk.Button(self.frame, text="Login", command=self.handle_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Existing users (if any)
        if existing_users:
            ttk.Label(self.frame, text="Existing users:", 
                     font=('Arial', 10)).grid(row=3, column=0, columnspan=2, pady=(20, 5))
            users_text = ", ".join(existing_users)
            ttk.Label(self.frame, text=users_text, font=('Arial', 9),
                     foreground='gray').grid(row=4, column=0, columnspan=2)
    
    def handle_login(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        if not username.replace('_', '').replace('-', '').isalnum():
            messagebox.showerror("Error", "Username can only contain letters, numbers, hyphens, and underscores")
            return
        self.on_login(username)
    
    def destroy(self):
        self.frame.destroy()


class MainMenu:
    """Main menu screen."""
    
    def __init__(self, root: tk.Tk, username: str, 
                 on_practice: Callable[[], None],
                 on_stats: Callable[[], None],
                 deck_metadata: DeckMetadata,
                 total_cards: int,
                 due_cards: int):
        self.root = root
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Welcome message
        welcome = ttk.Label(self.frame, text=f"Welcome, {username}!", 
                           font=('Arial', 20, 'bold'))
        welcome.grid(row=0, column=0, pady=20)
        
        # Stats summary
        stats_frame = ttk.LabelFrame(self.frame, text="Today's Progress", padding="10")
        stats_frame.grid(row=1, column=0, pady=20)
        
        today_count = deck_metadata.get_today_count()
        max_count = deck_metadata.max_per_day
        
        ttk.Label(stats_frame, text=f"Cards reviewed today: {today_count} / {max_count}",
                 font=('Arial', 12)).grid(row=0, column=0, pady=5)
        ttk.Label(stats_frame, text=f"Cards due for review: {due_cards}",
                 font=('Arial', 12)).grid(row=1, column=0, pady=5)
        ttk.Label(stats_frame, text=f"Total cards in deck: {total_cards}",
                 font=('Arial', 12)).grid(row=2, column=0, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=2, column=0, pady=20)
        
        practice_btn = ttk.Button(btn_frame, text="Practice Cards", 
                                 command=on_practice, width=20)
        practice_btn.grid(row=0, column=0, pady=10)
        
        stats_btn = ttk.Button(btn_frame, text="View Stats", 
                              command=on_stats, width=20)
        stats_btn.grid(row=1, column=0, pady=10)
    
    def destroy(self):
        self.frame.destroy()


class PracticeView:
    """Flashcard practice view with binary grading."""
    
    def __init__(self, root: tk.Tk, cards: list[Card],
                 on_grade: Callable[[Card, bool], None],
                 on_done: Callable[[], None]):
        self.root = root
        self.cards = cards
        self.on_grade = on_grade
        self.on_done = on_done
        self.current_index = 0
        self.show_answer = False
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress label
        self.progress_label = ttk.Label(self.frame, text="", font=('Arial', 10))
        self.progress_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Card display
        self.card_frame = ttk.Frame(self.frame, relief='solid', borderwidth=2)
        self.card_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=20, 
                            sticky=(tk.W, tk.E))
        
        self.card_text = ttk.Label(self.card_frame, text="", 
                                   font=('Arial', 48), anchor='center')
        self.card_text.grid(row=0, column=0, pady=50, padx=50)
        
        # Answer label (hidden initially)
        self.answer_label = ttk.Label(self.frame, text="", 
                                      font=('Arial', 24), foreground='blue')
        self.answer_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Show answer button
        self.show_btn = ttk.Button(self.frame, text="Show Answer", 
                                   command=self.show_answer_clicked)
        self.show_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Grading buttons (hidden initially)
        self.grade_frame = ttk.Frame(self.frame)
        self.grade_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.again_btn = ttk.Button(self.grade_frame, text="Again", 
                                    command=lambda: self.grade_clicked(True),
                                    width=15)
        self.again_btn.grid(row=0, column=0, padx=10)
        
        self.good_btn = ttk.Button(self.grade_frame, text="Good", 
                                   command=lambda: self.grade_clicked(False),
                                   width=15)
        self.good_btn.grid(row=0, column=1, padx=10)
        
        # Initially hide grading buttons
        self.grade_frame.grid_remove()
        
        # Bind keyboard shortcuts
        self.root.bind('<space>', lambda e: self.show_answer_clicked())
        self.root.bind('1', lambda e: self.grade_clicked(True) if self.show_answer else None)
        self.root.bind('2', lambda e: self.grade_clicked(False) if self.show_answer else None)
        
        # Display first card
        self.display_current_card()
    
    def display_current_card(self):
        """Display the current card."""
        if self.current_index >= len(self.cards):
            self.on_done()
            return
        
        card = self.cards[self.current_index]
        self.show_answer = False
        
        # Update progress
        self.progress_label.config(
            text=f"Card {self.current_index + 1} of {len(self.cards)}")
        
        # Show front of card
        self.card_text.config(text=card.front)
        self.answer_label.config(text="")
        
        # Show "Show Answer" button, hide grading buttons
        self.show_btn.grid()
        self.grade_frame.grid_remove()
    
    def show_answer_clicked(self):
        """Show the answer side of the card."""
        if self.show_answer:
            return
        
        self.show_answer = True
        card = self.cards[self.current_index]
        
        # Show answer
        self.answer_label.config(text=f"Answer: {card.back}")
        
        # Hide "Show Answer" button, show grading buttons
        self.show_btn.grid_remove()
        self.grade_frame.grid()
    
    def grade_clicked(self, grade_again: bool):
        """Handle grading button click."""
        if not self.show_answer:
            return
        
        card = self.cards[self.current_index]
        self.on_grade(card, grade_again)
        
        # Move to next card
        self.current_index += 1
        self.display_current_card()
    
    def destroy(self):
        # Unbind keyboard shortcuts
        self.root.unbind('<space>')
        self.root.unbind('1')
        self.root.unbind('2')
        self.frame.destroy()


class StatsView:
    """Statistics and insights view with FSRS-6 parameter display and manual intensity override."""
    
    def __init__(self, root: tk.Tk, cards: list[Card], 
                 deck_metadata: DeckMetadata, scheduler, settings, 
                 on_back: Callable[[], None],
                 on_intensity_changed: Callable[[], None]):
        self.root = root
        self.cards = cards
        self.deck_metadata = deck_metadata
        self.scheduler = scheduler
        self.settings = settings
        self.on_back = on_back
        self.on_intensity_changed = on_intensity_changed
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(self.frame, text="Statistics & Insights", 
                         font=('Arial', 20, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # FSRS-6 Parameters section (new)
        self._create_fsrs_parameters_section()
        
        # Calculate stats
        total_cards = len(cards)
        new_cards = sum(1 for c in cards if c.state == 0)
        learning_cards = sum(1 for c in cards if c.state == 1)
        review_cards = sum(1 for c in cards if c.state == 2)
        relearning_cards = sum(1 for c in cards if c.state == 3)
        
        avg_difficulty = sum(c.difficulty for c in cards) / total_cards if total_cards > 0 else 0
        avg_stability = sum(c.stability for c in cards if c.stability > 0) / max(1, sum(1 for c in cards if c.stability > 0))
        total_lapses = sum(c.lapses for c in cards)
        
        # Stats display
        stats_frame = ttk.LabelFrame(self.frame, text="Deck Statistics", padding="15")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        stats = [
            ("Total Cards:", total_cards),
            ("New Cards:", new_cards),
            ("Learning:", learning_cards),
            ("Review:", review_cards),
            ("Relearning:", relearning_cards),
            ("", ""),  # Spacer
            ("Average Difficulty:", f"{avg_difficulty:.1f} / 10"),
            ("Average Stability:", f"{avg_stability:.1f} days"),
            ("Total Lapses:", total_lapses),
        ]
        
        for i, (label, value) in enumerate(stats):
            if label:
                ttk.Label(stats_frame, text=label, font=('Arial', 11)).grid(
                    row=i, column=0, sticky=tk.W, pady=3)
                ttk.Label(stats_frame, text=str(value), font=('Arial', 11, 'bold')).grid(
                    row=i, column=1, sticky=tk.E, padx=20, pady=3)
        
        # Daily stats
        daily_frame = ttk.LabelFrame(self.frame, text="Daily Progress", padding="15")
        daily_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        today_count = deck_metadata.get_today_count()
        max_per_day = deck_metadata.max_per_day
        
        ttk.Label(daily_frame, text="Today's Reviews:", font=('Arial', 11)).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        ttk.Label(daily_frame, text=f"{today_count} / {max_per_day}", 
                 font=('Arial', 11, 'bold')).grid(row=0, column=1, sticky=tk.E, padx=20, pady=3)
        
        # Recent activity
        if deck_metadata.daily_counts:
            recent_frame = ttk.LabelFrame(self.frame, text="Recent Activity", padding="15")
            recent_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
            
            # Sort dates and show last 7 days
            sorted_dates = sorted(deck_metadata.daily_counts.items(), reverse=True)[:7]
            for i, (date, count) in enumerate(sorted_dates):
                ttk.Label(recent_frame, text=date, font=('Arial', 10)).grid(
                    row=i, column=0, sticky=tk.W, pady=2)
                ttk.Label(recent_frame, text=f"{count} cards", 
                         font=('Arial', 10)).grid(row=i, column=1, sticky=tk.E, padx=20, pady=2)
        
        # Back button
        back_btn = ttk.Button(self.frame, text="Back to Menu", 
                             command=on_back, width=20)
        back_btn.grid(row=5, column=0, pady=20)
    
    def _create_fsrs_parameters_section(self):
        """Create FSRS-6 parameters display and manual intensity override controls."""
        params_frame = ttk.LabelFrame(self.frame, text="FSRS-6 Learning Parameters", padding="15")
        params_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Get current parameters
        params = self.scheduler.get_current_parameters()
        intensity = params['intensity']
        stability_growth = params['stabilityGrowth']
        diff_adjust = params['diffAdjust']
        retention = params['request_retention']
        
        # Check if manual override is active
        is_manual = self.settings.is_manual_override_active()
        intensity_display = f"{intensity:.2f}"
        if is_manual:
            intensity_display += " (manual)"
        
        # Display current parameters
        row = 0
        ttk.Label(params_frame, text="Intensity:", font=('Arial', 11)).grid(
            row=row, column=0, sticky=tk.W, pady=3)
        ttk.Label(params_frame, text=intensity_display, 
                 font=('Arial', 11, 'bold')).grid(row=row, column=1, sticky=tk.E, padx=20, pady=3)
        
        row += 1
        ttk.Label(params_frame, text="Stability Growth:", font=('Arial', 11)).grid(
            row=row, column=0, sticky=tk.W, pady=3)
        ttk.Label(params_frame, text=f"{stability_growth:.3f}", 
                 font=('Arial', 11, 'bold')).grid(row=row, column=1, sticky=tk.E, padx=20, pady=3)
        
        row += 1
        ttk.Label(params_frame, text="Difficulty Adjust:", font=('Arial', 11)).grid(
            row=row, column=0, sticky=tk.W, pady=3)
        ttk.Label(params_frame, text=f"{diff_adjust:.3f}", 
                 font=('Arial', 11, 'bold')).grid(row=row, column=1, sticky=tk.E, padx=20, pady=3)
        
        row += 1
        ttk.Label(params_frame, text="Target Retention:", font=('Arial', 11)).grid(
            row=row, column=0, sticky=tk.W, pady=3)
        ttk.Label(params_frame, text=f"{retention:.0%}", 
                 font=('Arial', 11, 'bold')).grid(row=row, column=1, sticky=tk.E, padx=20, pady=3)
        
        # Manual intensity override controls
        row += 1
        ttk.Separator(params_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        row += 1
        ttk.Label(params_frame, text="Manual Intensity Override:", 
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(5, 3))
        
        row += 1
        control_frame = ttk.Frame(params_frame)
        control_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(control_frame, text="Intensity (0-10+):", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
        
        # Spinbox for intensity input
        self.intensity_var = tk.StringVar(value=f"{intensity:.1f}" if is_manual else "")
        self.intensity_spinbox = ttk.Spinbox(
            control_frame, 
            from_=0.0, 
            to=15.0, 
            increment=0.5,
            textvariable=self.intensity_var,
            width=10
        )
        self.intensity_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Apply button
        self.apply_btn = ttk.Button(
            control_frame, 
            text="Apply", 
            command=self._apply_manual_intensity,
            width=10
        )
        self.apply_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear override button
        if is_manual:
            clear_btn = ttk.Button(
                control_frame,
                text="Clear Override",
                command=self._clear_manual_intensity,
                width=12
            )
            clear_btn.pack(side=tk.LEFT, padx=5)
        
        row += 1
        ttk.Label(params_frame, 
                 text="Note: Higher intensity = more frequent reviews, faster learning",
                 font=('Arial', 9), foreground='gray').grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
    
    def _apply_manual_intensity(self):
        """Apply manual intensity override."""
        try:
            value_str = self.intensity_var.get().strip()
            if not value_str:
                messagebox.showerror("Error", "Please enter an intensity value")
                return
            
            value = float(value_str)
            
            if value < 0:
                messagebox.showerror("Error", "Intensity must be >= 0")
                return
            
            if value > 10:
                response = messagebox.askyesno(
                    "Warning",
                    f"Intensity {value:.1f} is very high (>10).\n\n"
                    "This will result in very frequent reviews and may be overwhelming.\n\n"
                    "The value will be capped at 10.0. Continue?"
                )
                if not response:
                    return
                value = 10.0
                self.intensity_var.set(f"{value:.1f}")
            
            # Apply the override
            self.settings.set_manual_intensity(value)
            
            # Notify parent to reload with new intensity
            messagebox.showinfo("Success", 
                              f"Manual intensity override set to {value:.1f}\n\n"
                              "Returning to menu to apply changes.")
            self.on_intensity_changed()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def _clear_manual_intensity(self):
        """Clear manual intensity override."""
        response = messagebox.askyesno(
            "Clear Override",
            "Clear manual intensity override and return to minutes-based intensity?\n\n"
            f"Minutes/day: {self.settings.minutes_per_day} → "
            f"Intensity: {self.settings.minutes_to_intensity(self.settings.minutes_per_day):.2f}"
        )
        if response:
            self.settings.set_manual_intensity(None)
            messagebox.showinfo("Success", "Manual override cleared. Returning to menu.")
            self.on_intensity_changed()
    
    def destroy(self):
        self.frame.destroy()
