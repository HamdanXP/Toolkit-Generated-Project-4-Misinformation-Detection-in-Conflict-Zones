import tkinter as tk
from tkinter import ttk, scrolledtext
import logging

class MisinformationGUI:
    def __init__(self, detector):
        self.detector = detector
        self.logger = logging.getLogger(__name__)
        
        # Create main window
        self.root = tk.Tk()
        self.root.title('Misinformation Detector')
        self.root.geometry('800x600')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text='Input Text', padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(input_frame, height=10)
        self.text_input.pack(fill='x')
        
        # URL frame
        url_frame = ttk.LabelFrame(self.root, text='Source URL (Optional)', padding=10)
        url_frame.pack(fill='x', padx=10, pady=5)
        
        self.url_input = ttk.Entry(url_frame)
        self.url_input.pack(fill='x')
        
        # Analysis button
        analyze_btn = ttk.Button(self.root, text='Analyze Text', command=self.analyze)
        analyze_btn.pack(pady=10)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.root, text='Analysis Results', padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10)
        self.results_text.pack(fill='both', expand=True)
        
    def analyze(self):
        """Handle analysis button click"""
        try:
            text = self.text_input.get('1.0', tk.END).strip()
            url = self.url_input.get().strip()
            
            if not text:
                self.show_error('Please enter some text to analyze')
                return
                
            # Get analysis results
            results = self.detector.analyze_text(text, url if url else None)
            
            # Display results
            self.display_results(results)
            
        except Exception as e:
            self.logger.error(f'Error during analysis: {e}')
            self.show_error('An error occurred during analysis')
            
    def display_results(self, results):
        """Display analysis results"""
        self.results_text.delete('1.0', tk.END)
        
        # Display risk score
        risk_percent = int(results['risk_score'] * 100)
        self.results_text.insert(tk.END, f'Risk Score: {risk_percent}%\n\n')
        
        # Display credibility score if available
        if results['credibility_score'] is not None:
            cred_percent = int(results['credibility_score'] * 100)
            self.results_text.insert(tk.END, f'Source Credibility: {cred_percent}%\n\n')
            
        # Display explanation
        self.results_text.insert(tk.END, 'Analysis Details:\n')
        for point in results['explanation']:
            self.results_text.insert(tk.END, f'• {point}\n')
            
    def show_error(self, message):
        """Display error message"""
        tk.messagebox.showerror('Error', message)
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()