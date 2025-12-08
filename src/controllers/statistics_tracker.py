"""
StatisticsTracker Class - Mood analytics and visualization

This class demonstrates:
- Data analysis using pandas
- Chart generation using matplotlib
- ENCAPSULATION of analytics logic

Requires: matplotlib, pandas
Install with: pip install matplotlib pandas

Author: [Nama Kamu]
Date: December 2025
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import os


class StatisticsTracker:
    """
    Tracks and visualizes mood statistics.
    
    Attributes:
        __mood_history: Reference to user's mood history
        __analytics_data (dict): Cached analytics data
    """
    
    def __init__(self):
        """Initialize StatisticsTracker."""
        # ENCAPSULATION: Private attributes
        self.__mood_history = []
        self.__analytics_data = {}
    
    # ==================== DATA LOADING ====================
    
    def load_mood_history(self, mood_history):
        """
        Load mood history data for analysis.
        
        Args:
            mood_history (list): List of mood records
        """
        self.__mood_history = mood_history
        self.__analytics_data = {}  # Clear cache
        print(f"✓ Loaded {len(mood_history)} mood records for analysis")
    
    # ==================== STATISTICS CALCULATION ====================
    
    def get_most_common_emotion(self):
        """
        Get the most frequently recorded emotion.
        
        Returns:
            tuple: (emotion_type, count) or (None, 0) if no data
        """
        if not self.__mood_history:
            return (None, 0)
        
        emotions = [record['emotion_type'] for record in self.__mood_history]
        counter = Counter(emotions)
        most_common = counter.most_common(1)[0]
        
        return most_common
    
    def get_emotion_distribution(self):
        """
        Get distribution of all emotions.
        
        Returns:
            dict: Emotion -> count mapping
        """
        if not self.__mood_history:
            return {}
        
        emotions = [record['emotion_type'] for record in self.__mood_history]
        return dict(Counter(emotions))
    
    def get_daily_mood_summary(self, date=None):
        """
        Get mood summary for a specific date.
        
        Args:
            date (datetime.date): Date to analyze (default: today)
            
        Returns:
            dict: Summary statistics
        """
        if date is None:
            date = datetime.now().date()
        
        # Filter records for this date
        daily_records = [
            record for record in self.__mood_history
            if record['timestamp'].date() == date
        ]
        
        if not daily_records:
            return {
                'date': date.isoformat(),
                'total_records': 0,
                'emotions': {},
                'average_intensity': 0
            }
        
        # Calculate statistics
        emotions = [r['emotion_type'] for r in daily_records]
        intensities = [r['intensity'] for r in daily_records]
        
        return {
            'date': date.isoformat(),
            'total_records': len(daily_records),
            'emotions': dict(Counter(emotions)),
            'average_intensity': round(sum(intensities) / len(intensities), 2),
            'most_common': Counter(emotions).most_common(1)[0][0]
        }
    
    def get_weekly_report(self, end_date=None):
        """
        Get mood report for the past 7 days.
        
        Args:
            end_date (datetime.date): End date (default: today)
            
        Returns:
            dict: Weekly statistics
        """
        if end_date is None:
            end_date = datetime.now().date()
        
        start_date = end_date - timedelta(days=6)
        
        # Filter records for this week
        weekly_records = [
            record for record in self.__mood_history
            if start_date <= record['timestamp'].date() <= end_date
        ]
        
        if not weekly_records:
            return {
                'period': f"{start_date} to {end_date}",
                'total_records': 0,
                'daily_breakdown': {}
            }
        
        # Group by date
        daily_breakdown = {}
        current_date = start_date
        
        while current_date <= end_date:
            day_records = [
                r for r in weekly_records
                if r['timestamp'].date() == current_date
            ]
            
            if day_records:
                emotions = [r['emotion_type'] for r in day_records]
                daily_breakdown[current_date.isoformat()] = {
                    'count': len(day_records),
                    'most_common': Counter(emotions).most_common(1)[0][0]
                }
            else:
                daily_breakdown[current_date.isoformat()] = {
                    'count': 0,
                    'most_common': None
                }
            
            current_date += timedelta(days=1)
        
        return {
            'period': f"{start_date} to {end_date}",
            'total_records': len(weekly_records),
            'daily_breakdown': daily_breakdown,
            'most_common_overall': self._get_most_common_from_records(weekly_records)
        }
    
    def get_listening_patterns(self):
        """
        Analyze listening patterns by time of day.
        
        Returns:
            dict: Time of day -> count mapping
        """
        if not self.__mood_history:
            return {}
        
        times = [record.get('time_of_day', 'unknown') for record in self.__mood_history]
        return dict(Counter(times))
    
    # ==================== CHART GENERATION ====================
    
    def generate_mood_chart(self, output_path='screenshots/mood_chart.png', days=7):
        """
        Generate bar chart of mood distribution over time.
        
        Args:
            output_path (str): Path to save chart
            days (int): Number of days to include
            
        Returns:
            bool: True if successful
        """
        if not self.__mood_history:
            print("⚠ No mood data to chart")
            return False
        
        try:
            # Prepare data
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days-1)
            
            # Filter recent records
            recent_records = [
                r for r in self.__mood_history
                if start_date <= r['timestamp'].date() <= end_date
            ]
            
            if not recent_records:
                print(f"⚠ No data for the past {days} days")
                return False
            
            # Group by date and emotion
            daily_data = {}
            current_date = start_date
            
            while current_date <= end_date:
                day_str = current_date.strftime('%m/%d')
                day_records = [
                    r for r in recent_records
                    if r['timestamp'].date() == current_date
                ]
                
                if day_records:
                    emotions = [r['emotion_type'] for r in day_records]
                    daily_data[day_str] = Counter(emotions)
                else:
                    daily_data[day_str] = Counter()
                
                current_date += timedelta(days=1)
            
            # Create DataFrame
            df = pd.DataFrame(daily_data).fillna(0).T
            
            # Plot
            plt.figure(figsize=(12, 6))
            df.plot(kind='bar', stacked=False, colormap='viridis')
            
            plt.title(f'Mood Distribution - Past {days} Days', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Number of Records', fontsize=12)
            plt.legend(title='Emotions', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✓ Chart saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error generating chart: {e}")
            return False
    
    def generate_emotion_pie_chart(self, output_path='screenshots/emotion_pie.png'):
        """
        Generate pie chart of overall emotion distribution.
        
        Args:
            output_path (str): Path to save chart
            
        Returns:
            bool: True if successful
        """
        if not self.__mood_history:
            print("⚠ No mood data to chart")
            return False
        
        try:
            # Get distribution
            distribution = self.get_emotion_distribution()
            
            # Plot
            plt.figure(figsize=(10, 8))
            plt.pie(
                distribution.values(),
                labels=distribution.keys(),
                autopct='%1.1f%%',
                startangle=90,
                colors=plt.cm.Set3.colors
            )
            
            plt.title('Overall Emotion Distribution', fontsize=16, fontweight='bold')
            plt.axis('equal')
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✓ Pie chart saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error generating pie chart: {e}")
            return False
    
    def generate_intensity_timeline(self, output_path='screenshots/intensity_timeline.png', days=7):
        """
        Generate line chart showing intensity over time.
        
        Args:
            output_path (str): Path to save chart
            days (int): Number of days to include
            
        Returns:
            bool: True if successful
        """
        if not self.__mood_history:
            print("⚠ No mood data to chart")
            return False
        
        try:
            # Filter recent records
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            recent_records = [
                r for r in self.__mood_history
                if start_date <= r['timestamp'] <= end_date
            ]
            
            if not recent_records:
                print(f"⚠ No data for the past {days} days")
                return False
            
            # Extract timestamps and intensities
            timestamps = [r['timestamp'] for r in recent_records]
            intensities = [r['intensity'] for r in recent_records]
            
            # Plot
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, intensities, marker='o', linestyle='-', linewidth=2, markersize=8)
            
            plt.title(f'Emotion Intensity Timeline - Past {days} Days', fontsize=16, fontweight='bold')
            plt.xlabel('Date/Time', fontsize=12)
            plt.ylabel('Intensity (1-10)', fontsize=12)
            plt.ylim(0, 11)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✓ Timeline saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error generating timeline: {e}")
            return False
    
    # ==================== DATA EXPORT ====================
    
    def export_statistics_csv(self, output_path='data/mood_statistics.csv'):
        """
        Export statistics to CSV file.
        
        Args:
            output_path (str): Path to save CSV
            
        Returns:
            bool: True if successful
        """
        if not self.__mood_history:
            print("⚠ No data to export")
            return False
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(self.__mood_history)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Export
            df.to_csv(output_path, index=False)
            
            print(f"✓ Statistics exported to {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error exporting CSV: {e}")
            return False
    
    # ==================== PRIVATE HELPER METHODS ====================
    
    def _get_most_common_from_records(self, records):
        """
        Get most common emotion from a list of records.
        
        Args:
            records (list): Mood records
            
        Returns:
            str: Most common emotion or None
        """
        if not records:
            return None
        
        emotions = [r['emotion_type'] for r in records]
        return Counter(emotions).most_common(1)[0][0]
    
    # ==================== STRING REPRESENTATION ====================
    
    def __str__(self):
        """String representation."""
        return f"StatisticsTracker ({len(self.__mood_history)} records)"


# ==================== TESTING ====================
if __name__ == "__main__":
    print("Testing StatisticsTracker Class...")
    print("=" * 60)
    
    # Create dummy data
    print("\n--- Creating Test Data ---")
    tracker = StatisticsTracker()
    
    # Dummy mood records
    dummy_data = [
        {'emotion_type': 'happy', 'intensity': 8, 'timestamp': datetime.now() - timedelta(days=2), 'time_of_day': 'morning'},
        {'emotion_type': 'happy', 'intensity': 7, 'timestamp': datetime.now() - timedelta(days=1), 'time_of_day': 'afternoon'},
        {'emotion_type': 'sad', 'intensity': 4, 'timestamp': datetime.now(), 'time_of_day': 'evening'},
    ]
    
    tracker.load_mood_history(dummy_data)
    
    # Test statistics
    print("\n--- Testing Statistics ---")
    print(f"Most common emotion: {tracker.get_most_common_emotion()}")
    print(f"Distribution: {tracker.get_emotion_distribution()}")
    print(f"Listening patterns: {tracker.get_listening_patterns()}")
    
    print("\n" + "=" * 60)
    print("✓ Basic tests completed!")
    print("Note: Chart generation requires matplotlib")