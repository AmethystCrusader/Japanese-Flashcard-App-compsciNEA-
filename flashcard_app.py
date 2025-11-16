#!/usr/bin/env python3
"""
Japanese Flashcard Application with FSRS-6 Scheduler
Main entry point for the application.
"""
import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

from models import Card, DeckMetadata
from fsrs import FSRS6Scheduler
from persistence import PersistenceManager
from gui import LoginScreen, MainMenu, PracticeView, StatsView


class FlashcardApp:
    """Main application controller."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Japanese Flashcard App - FSRS-6")
        self.root.geometry("700x600")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Initialize components
        self.scheduler = FSRS6Scheduler()
        self.persistence = PersistenceManager()
        
        # Application state
        self.current_user: str = None
        self.deck_name = "hiragana"
        self.csv_path = "hiragana.csv"
        self.cards: list[Card] = []
        self.deck_metadata: DeckMetadata = None
        
        # Current view
        self.current_view = None
        
        # Start with login screen
        self.show_login_screen()
    
    def show_login_screen(self):
        """Display the login screen."""
        if self.current_view:
            self.current_view.destroy()
        
        existing_users = self.persistence.list_users()
        self.current_view = LoginScreen(
            self.root,
            on_login=self.handle_login,
            existing_users=existing_users
        )
    
    def handle_login(self, username: str):
        """Handle user login."""
        self.current_user = username
        
        # Create user if doesn't exist
        if not self.persistence.user_exists(username):
            self.persistence.create_user(username)
        
        # Load deck
        self.load_deck()
        
        # Show main menu
        self.show_main_menu()
    
    def load_deck(self):
        """Load the deck from CSV and metadata."""
        try:
            self.cards = self.persistence.load_deck_from_csv(
                self.csv_path, 
                self.current_user, 
                self.deck_name
            )
            self.deck_metadata = self.persistence.load_deck_metadata(
                self.current_user, 
                self.deck_name
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load deck: {e}")
            sys.exit(1)
    
    def save_deck(self):
        """Save the deck and metadata."""
        try:
            # Save card metadata
            self.persistence.save_card_metadata(
                self.current_user, 
                self.deck_name, 
                self.cards
            )
            
            # Save deck metadata
            self.persistence.save_deck_metadata(
                self.current_user, 
                self.deck_name, 
                self.deck_metadata
            )
            
            # Save CSV (optional, updates state and lastSeen)
            self.persistence.save_deck_to_csv(self.csv_path, self.cards)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save deck: {e}")
    
    def show_main_menu(self):
        """Display the main menu."""
        if self.current_view:
            self.current_view.destroy()
        
        due_cards = len(self.scheduler.get_due_cards(self.cards))
        
        self.current_view = MainMenu(
            self.root,
            username=self.current_user,
            on_practice=self.show_practice_view,
            on_stats=self.show_stats_view,
            deck_metadata=self.deck_metadata,
            total_cards=len(self.cards),
            due_cards=due_cards
        )
    
    def show_practice_view(self):
        """Display the practice view."""
        # Get due cards
        due_cards = self.scheduler.get_due_cards(self.cards)
        
        # Check daily limit
        if not due_cards:
            messagebox.showinfo("No Cards Due", 
                              "No cards are due for review right now!")
            return
        
        if not self.deck_metadata.can_review_more():
            response = messagebox.askyesno(
                "Daily Limit Reached",
                f"You've reached your daily limit of {self.deck_metadata.max_per_day} cards.\n\n"
                "Do you want to continue reviewing anyway?"
            )
            if response:
                self.deck_metadata.allow_over_limit_today = True
            else:
                return
        
        # Limit cards to review based on daily limit
        remaining = self.deck_metadata.max_per_day - self.deck_metadata.get_today_count()
        if remaining > 0 and not self.deck_metadata.allow_over_limit_today:
            due_cards = due_cards[:remaining]
        
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = PracticeView(
            self.root,
            cards=due_cards,
            on_grade=self.handle_grade,
            on_done=self.handle_practice_done
        )
    
    def handle_grade(self, card: Card, grade_again: bool):
        """Handle card grading."""
        # Update card with FSRS-6
        self.scheduler.schedule_card(card, grade_again)
        
        # Increment daily count
        self.deck_metadata.increment_today_count()
        
        # Save after each card
        self.save_deck()
    
    def handle_practice_done(self):
        """Handle completion of practice session."""
        messagebox.showinfo("Session Complete", 
                          "Great job! You've completed this practice session.")
        self.show_main_menu()
    
    def show_stats_view(self):
        """Display the statistics view."""
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = StatsView(
            self.root,
            cards=self.cards,
            deck_metadata=self.deck_metadata,
            on_back=self.show_main_menu
        )
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    # Check if hiragana.csv exists
    if not Path("hiragana.csv").exists():
        print("Error: hiragana.csv not found in current directory")
        sys.exit(1)
    
    app = FlashcardApp()
    app.run()


if __name__ == "__main__":
    main()
