"""
Application Tracking System
Track job applications, which CV versions were sent, and follow-ups
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


class ApplicationTracker:
    """Track and manage job applications with analytics."""
    
    def __init__(self, tracker_file: str = "applications_tracker.json"):
        """Initialize tracker."""
        self.tracker_file = tracker_file
        self.applications = self._load_tracker()
    
    def _load_tracker(self) -> list:
        """Load applications from tracker file."""
        try:
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_tracker(self):
        """Save applications to tracker file."""
        with open(self.tracker_file, 'w') as f:
            json.dump(self.applications, f, indent=2)
    
    def add_application(self,
                       position: str,
                       company: str,
                       application_type: str = "academic",
                       cv_version: str = None,
                       cover_letter: str = None,
                       deadline: str = None,
                       contact_person: str = None,
                       contact_email: str = None,
                       salary_range: str = None,
                       location: str = None,
                       job_url: str = None,
                       notes: str = None) -> dict:
        """
        Add a new application to tracker.
        
        Returns:
            The created application dict
        """
        application = {
            "id": len(self.applications) + 1,
            "position": position,
            "company": company,
            "type": application_type,
            "cv_version": cv_version,
            "cover_letter": cover_letter,
            "status": "submitted",
            "date_applied": datetime.now().isoformat(),
            "deadline": deadline,
            "contact_person": contact_person,
            "contact_email": contact_email,
            "salary_range": salary_range,
            "location": location,
            "job_url": job_url,
            "notes": notes or "",
            "follow_ups": [],
            "interviews": [],
            "outcome": None,
            "outcome_date": None
        }
        
        self.applications.append(application)
        self._save_tracker()
        
        print(f"✓ Added application #{application['id']}: {position} at {company}")
        return application
    
    def update_status(self, app_id: int, new_status: str, notes: str = None):
        """
        Update application status.
        
        Status options: submitted, under_review, interview_scheduled, 
                       interviewed, offered, rejected, withdrawn, accepted
        """
        valid_statuses = [
            "submitted", "under_review", "interview_scheduled",
            "interviewed", "offered", "rejected", "withdrawn", "accepted"
        ]
        
        if new_status not in valid_statuses:
            print(f"⚠️  Invalid status. Valid options: {', '.join(valid_statuses)}")
            return
        
        app = self._get_application(app_id)
        if app:
            app["status"] = new_status
            app["last_updated"] = datetime.now().isoformat()
            
            if notes:
                app["notes"] += f"\n[{datetime.now().strftime('%Y-%m-%d')}] {notes}"
            
            # Set outcome if final status
            if new_status in ["offered", "rejected", "withdrawn", "accepted"]:
                app["outcome"] = new_status
                app["outcome_date"] = datetime.now().isoformat()
            
            self._save_tracker()
            print(f"✓ Updated application #{app_id} status to: {new_status}")
    
    def add_follow_up(self, app_id: int, method: str = "email", notes: str = ""):
        """Record a follow-up action."""
        app = self._get_application(app_id)
        if app:
            follow_up = {
                "date": datetime.now().isoformat(),
                "method": method,  # email, phone, linkedin, etc.
                "notes": notes
            }
            app["follow_ups"].append(follow_up)
            self._save_tracker()
            print(f"✓ Added follow-up for application #{app_id}")
    
    def add_interview(self, app_id: int, 
                     interview_date: str,
                     interview_type: str = "initial",
                     interviewers: str = None,
                     notes: str = None):
        """Record an interview."""
        app = self._get_application(app_id)
        if app:
            interview = {
                "date": interview_date,
                "type": interview_type,  # initial, technical, panel, final, etc.
                "interviewers": interviewers,
                "notes": notes,
                "recorded_at": datetime.now().isoformat()
            }
            app["interviews"].append(interview)
            app["status"] = "interviewed"
            self._save_tracker()
            print(f"✓ Added interview for application #{app_id}")
    
    def _get_application(self, app_id: int) -> Optional[dict]:
        """Get application by ID."""
        for app in self.applications:
            if app["id"] == app_id:
                return app
        print(f"❌ Application #{app_id} not found")
        return None
    
    def list_applications(self, 
                         status: str = None,
                         company: str = None,
                         app_type: str = None) -> List[dict]:
        """
        List applications with optional filters.
        
        Args:
            status: Filter by status
            company: Filter by company name (partial match)
            app_type: Filter by application type
        """
        filtered = self.applications
        
        if status:
            filtered = [a for a in filtered if a["status"] == status]
        
        if company:
            filtered = [a for a in filtered 
                       if company.lower() in a["company"].lower()]
        
        if app_type:
            filtered = [a for a in filtered if a["type"] == app_type]
        
        return filtered
    
    def get_applications_needing_followup(self, days: int = 14) -> List[dict]:
        """Get applications that might need a follow-up."""
        cutoff_date = datetime.now() - timedelta(days=days)
        needs_followup = []
        
        for app in self.applications:
            # Skip if final outcome reached
            if app.get("outcome") in ["rejected", "withdrawn", "accepted"]:
                continue
            
            # Check if last follow-up was too long ago
            if app["follow_ups"]:
                last_followup = datetime.fromisoformat(app["follow_ups"][-1]["date"])
                if last_followup < cutoff_date:
                    needs_followup.append(app)
            else:
                # No follow-ups yet and application is old
                applied_date = datetime.fromisoformat(app["date_applied"])
                if applied_date < cutoff_date:
                    needs_followup.append(app)
        
        return needs_followup
    
    def get_upcoming_deadlines(self, days: int = 7) -> List[dict]:
        """Get applications with upcoming deadlines."""
        upcoming = []
        cutoff_date = datetime.now() + timedelta(days=days)
        
        for app in self.applications:
            if app.get("deadline"):
                try:
                    deadline = datetime.fromisoformat(app["deadline"])
                    if datetime.now() < deadline < cutoff_date:
                        upcoming.append(app)
                except:
                    pass
        
        return sorted(upcoming, key=lambda x: x["deadline"])
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of all applications."""
        report = []
        report.append("=" * 70)
        report.append("APPLICATION TRACKER SUMMARY")
        report.append("=" * 70)
        
        # Overall stats
        total = len(self.applications)
        report.append(f"\n📊 Total Applications: {total}")
        
        if not total:
            report.append("\nNo applications tracked yet.")
            return "\n".join(report)
        
        # Status breakdown
        report.append("\n📈 Status Breakdown:")
        status_counts = {}
        for app in self.applications:
            status = app["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items()):
            percentage = (count / total) * 100
            report.append(f"   {status.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        
        # Outcomes
        outcomes = [a for a in self.applications if a.get("outcome")]
        if outcomes:
            report.append(f"\n🎯 Outcomes: {len(outcomes)} applications concluded")
            outcome_counts = {}
            for app in outcomes:
                outcome = app["outcome"]
                outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
            
            for outcome, count in sorted(outcome_counts.items()):
                report.append(f"   {outcome.title()}: {count}")
        
        # Application types
        report.append("\n📋 Application Types:")
        type_counts = {}
        for app in self.applications:
            app_type = app["type"]
            type_counts[app_type] = type_counts.get(app_type, 0) + 1
        
        for app_type, count in sorted(type_counts.items()):
            report.append(f"   {app_type.title()}: {count}")
        
        # CV versions used
        report.append("\n📄 CV Versions Used:")
        cv_counts = {}
        for app in self.applications:
            if app.get("cv_version"):
                cv = app["cv_version"]
                cv_counts[cv] = cv_counts.get(cv, 0) + 1
        
        for cv, count in sorted(cv_counts.items(), key=lambda x: x[1], reverse=True):
            report.append(f"   {cv}: {count} times")
        
        # Follow-ups needed
        needs_followup = self.get_applications_needing_followup()
        if needs_followup:
            report.append(f"\n⚠️  {len(needs_followup)} applications may need follow-up:")
            for app in needs_followup[:5]:
                days_ago = (datetime.now() - datetime.fromisoformat(app["date_applied"])).days
                report.append(f"   #{app['id']} {app['position']} at {app['company']} ({days_ago} days ago)")
        
        # Upcoming deadlines
        upcoming = self.get_upcoming_deadlines(14)
        if upcoming:
            report.append(f"\n📅 Upcoming Deadlines ({len(upcoming)}):")
            for app in upcoming:
                deadline = datetime.fromisoformat(app["deadline"])
                days_until = (deadline - datetime.now()).days
                report.append(f"   #{app['id']} {app['position']} at {app['company']} - {days_until} days")
        
        # Recent activity
        report.append("\n🕐 Recent Activity (Last 5):")
        recent = sorted(self.applications, 
                       key=lambda x: x.get("last_updated", x["date_applied"]),
                       reverse=True)[:5]
        
        for app in recent:
            date = app.get("last_updated", app["date_applied"])
            date_obj = datetime.fromisoformat(date)
            date_str = date_obj.strftime("%Y