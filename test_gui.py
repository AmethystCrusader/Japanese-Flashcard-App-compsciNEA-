#!/usr/bin/env python3
"""
GUI test script with screenshots.
Automated testing of the Tkinter GUI.
"""
import tkinter as tk
from PIL import Image, ImageGrab
import time
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flashcard_app import FlashcardApp
from models import Card


def take_screenshot(widget, filename):
    """Take a screenshot of a widget."""
    try:
        # Update the widget to ensure it's fully rendered
        widget.update_idletasks()
        widget.update()
        
        # Get widget position and size
        x = widget.winfo_rootx()
        y = widget.winfo_rooty()
        w = widget.winfo_width()
        h = widget.winfo_height()
        
        # Take screenshot
        import subprocess
        subprocess.run([
            'import', '-window', 'root', '-crop', f'{w}x{h}+{x}+{y}',
            filename
        ], check=False)
        
        print(f"Screenshot saved: {filename}")
        return True
    except Exception as e:
        print(f"Could not take screenshot: {e}")
        return False


def simulate_gui_interaction():
    """Simulate user interaction with the GUI."""
    print("Starting GUI test...")
    
    app = FlashcardApp()
    
    # Wait for window to render
    app.root.update()
    time.sleep(1)
    
    # Screenshot 1: Login screen
    print("Step 1: Login screen")
    take_screenshot(app.root, "/tmp/screenshot_login.png")
    
    # Simulate login
    if hasattr(app.current_view, 'username_var'):
        app.current_view.username_var.set("test_user")
        app.root.update()
        time.sleep(0.5)
        app.current_view.handle_login()
        app.root.update()
        time.sleep(1)
    
    # Screenshot 2: Main menu
    print("Step 2: Main menu")
    take_screenshot(app.root, "/tmp/screenshot_menu.png")
    
    # Click practice
    if hasattr(app.current_view, 'frame'):
        app.show_practice_view()
        app.root.update()
        time.sleep(1)
        
        # Screenshot 3: Practice view (question)
        print("Step 3: Practice view - question")
        take_screenshot(app.root, "/tmp/screenshot_practice_question.png")
        
        # Show answer
        if hasattr(app.current_view, 'show_answer_clicked'):
            app.current_view.show_answer_clicked()
            app.root.update()
            time.sleep(1)
            
            # Screenshot 4: Practice view (answer)
            print("Step 4: Practice view - answer")
            take_screenshot(app.root, "/tmp/screenshot_practice_answer.png")
            
            # Grade as Good
            if len(app.current_view.cards) > 0:
                card = app.current_view.cards[0]
                app.handle_grade(card, False)
                app.root.update()
                time.sleep(0.5)
    
    # Go back to menu
    app.show_main_menu()
    app.root.update()
    time.sleep(1)
    
    # Click stats
    app.show_stats_view()
    app.root.update()
    time.sleep(1)
    
    # Screenshot 5: Stats view
    print("Step 5: Stats view")
    take_screenshot(app.root, "/tmp/screenshot_stats.png")
    
    print("GUI test completed!")
    
    # Close the app
    app.root.after(1000, app.root.destroy)
    app.root.mainloop()


if __name__ == "__main__":
    simulate_gui_interaction()
