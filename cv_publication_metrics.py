"""
Publication Metrics Module
Fetches citation counts and metrics from various sources
Requires: scholarly, requests
Install: pip install scholarly requests
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import requests
from scholarly import scholarly
from cv_generator import CVGenerator


class PublicationMetrics:
    """Track and fetch publication metrics (citations, h-index, etc.)."""
    
    def __init__(self, cv_generator: CVGenerator, cache_file: str = "publication_metrics.json"):
        """Initialize with CV generator."""
        self.cv = cv_generator
        self.cache_file = cache_file
        self.metrics = self._load_cache()
    
    def _load_cache(self) -> dict:
        """Load cached metrics."""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "last_updated": None,
                "publications": {},
                "profile_metrics": {}
            }
    
    def _save_cache(self):
        """Save metrics to cache."""
        self.metrics["last_updated"] = datetime.now().isoformat()
        with open(self.cache_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def fetch_google_scholar_profile(self, scholar_id: str = None, 
                                     author_name: str = None):
        """
        Fetch profile metrics from Google Scholar.
        
        Args:
            scholar_id: Google Scholar ID (if known)
            author_name: Author name to search for
        """
        try:
            if scholar_id:
                author = scholarly.search_author_id(scholar_id)
            elif author_name:
                search_query = scholarly.search_author(author_name)
                author = next(search_query)
            else:
                author_name = self.cv.data['personal_info']['name']
                search_query = scholarly.search_author(author_name)
                author = next(search_query)
            
            author = scholarly.fill(author)
            
            # Extract metrics
            self.metrics["profile_metrics"]["google_scholar"] = {
                "name": author['name'],
                "affiliation": author.get('affiliation', ''),
                "citations_all": author.get('citedby', 0),
                "h_index": author.get('hindex', 0),
                "i10_index": author.get('i10index', 0),
                "scholar_id": author.get('scholar_id', ''),
                "interests": author.get('interests', []),
                "last_updated": datetime.now().isoformat()
            }
            
            print(f"✓ Fetched Google Scholar profile for {author['name']}")
            print(f"  Citations: {author.get('citedby', 0)}")
            print(f"  h-index: {author.get('hindex', 0)}")
            print(f"  i10-index: {author.get('i10index', 0)}")
            
            self._save_cache()
            return self.metrics["profile_metrics"]["google_scholar"]
            
        except Exception as e:
            print(f"❌ Error fetching Google Scholar profile: {e}")
            return None
    
    def fetch_publication_citations(self, publication_title: str, delay: int = 2):
        """
        Fetch citation count for a specific publication.
        
        Args:
            publication_title: Title of the publication
            delay: Delay between requests (to avoid rate limiting)
        """
        try:
            search_query = scholarly.search_pubs(publication_title)
            pub = next(search_query)
            
            # Get detailed info
            pub_filled = scholarly.fill(pub)
            
            citations = pub_filled.get('num_citations', 0)
            
            self.metrics["publications"][publication_title] = {
                "title": pub_filled.get('bib', {}).get('title', publication_title),
                "citations": citations,
                "year": pub_filled.get('bib', {}).get('pub_year', ''),
                "venue": pub_filled.get('bib', {}).get('venue', ''),
                "authors": pub_filled.get('bib', {}).get('author', ''),
                "url": pub_filled.get('pub_url', ''),
                "last_updated": datetime.now().isoformat()
            }
            
            print(f"✓ {publication_title}: {citations} citations")
            
            time.sleep(delay)  # Be nice to the API
            self._save_cache()
            
            return self.metrics["publications"][publication_title]
            
        except StopIteration:
            print(f"❌ Publication not found: {publication_title}")
            return None
        except Exception as e:
            print(f"❌ Error fetching citations for '{publication_title}': {e}")
            return None
    
    def fetch_all_publication_metrics(self, delay: int = 3):
        """Fetch metrics for all publications in CV."""
        print("\n=== Fetching Publication Metrics ===\n")
        
        all_pubs = []
        
        # Get conference proceedings
        for pub in self.cv.data['publications']['conference_proceedings']:
            all_pubs.append(pub['title'])
        
        # Get book chapters
        for pub in self.cv.data['publications']['book_chapters']:
            all_pubs.append(pub['title'])
        
        print(f"Found {len(all_pubs)} publications to check...\n")
        
        for i, title in enumerate(all_pubs, 1):
            print(f"[{i}/{len(all_pubs)}] Checking: {title[:60]}...")
            self.fetch_publication_citations(title, delay=delay)
        
        self._save_cache()
        print(f"\n✓ Metrics cached in {self.cache_file}")
    
    def fetch_orcid_metrics(self, orcid_id: str):
        """
        Fetch metrics from ORCID.
        
        Args:
            orcid_id: ORCID identifier (e.g., '0000-0002-7350-1987')
        """
        try:
            url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
            headers = {
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                works = data.get('group', [])
                
                self.metrics["profile_metrics"]["orcid"] = {
                    "orcid_id": orcid_id,
                    "total_works": len(works),
                    "last_updated": datetime.now().isoformat()
                }
                
                print(f"✓ Fetched ORCID profile")
                print(f"  Total works: {len(works)}")
                
                self._save_cache()
                return self.metrics["profile_metrics"]["orcid"]
            else:
                print(f"❌ ORCID API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching ORCID data: {e}")
            return None
    
    def generate_metrics_summary(self) -> str:
        """Generate a formatted summary of all metrics."""
        summary = []
        summary.append("=" * 60)
        summary.append("PUBLICATION METRICS SUMMARY")
        summary.append("=" * 60)
        
        # Profile metrics
        if "google_scholar" in self.metrics["profile_metrics"]:
            gs = self.metrics["profile_metrics"]["google_scholar"]
            summary.append("\n📊 Google Scholar Profile:")
            summary.append(f"   Total Citations: {gs['citations_all']}")
            summary.append(f"   h-index: {gs['h_index']}")
            summary.append(f"   i10-index: {gs['i10_index']}")
        
        if "orcid" in self.metrics["profile_metrics"]:
            orcid = self.metrics["profile_metrics"]["orcid"]
            summary.append(f"\n🔗 ORCID: {orcid['orcid_id']}")
            summary.append(f"   Registered works: {orcid['total_works']}")
        
        # Publication citations
        if self.metrics["publications"]:
            summary.append(f"\n📚 Individual Publications ({len(self.metrics['publications'])}):")
            summary.append("")
            
            # Sort by citations
            sorted_pubs = sorted(
                self.metrics["publications"].items(),
                key=lambda x: x[1].get('citations', 0),
                reverse=True
            )
            
            total_citations = sum(p[1].get('citations', 0) for p in sorted_pubs)
            
            for title, data in sorted_pubs[:10]:  # Top 10
                citations = data.get('citations', 0)
                year = data.get('year', 'N/A')
                summary.append(f"   [{citations:3d}] ({year}) {title[:50]}...")
            
            if len(sorted_pubs) > 10:
                summary.append(f"   ... and {len(sorted_pubs) - 10} more")
            
            summary.append(f"\n   Total Citations: {total_citations}")
        
        # Last updated
        if self.metrics.get("last_updated"):
            summary.append(f"\n⏰ Last updated: {self.metrics['last_updated']}")
        
        summary.append("=" * 60)
        
        return "\n".join(summary)
    
    def export_metrics_to_json(self, output_file: str = "metrics_export.json"):
        """Export metrics in a clean JSON format."""
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "profile": self.metrics.get("profile_metrics", {}),
            "publications": []
        }
        
        for title, data in self.metrics["publications"].items():
            export_data["publications"].append({
                "title": title,
                "citations": data.get("citations", 0),
                "year": data.get("year", ""),
                "venue": data.get("venue", ""),
                "url": data.get("url", "")
            })
        
        # Sort by citations
        export_data["publications"].sort(
            key=lambda x: x["citations"],
            reverse=True
        )
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✓ Metrics exported to {output_file}")
    
    def add_metrics_to_cv_data(self):
        """Add metrics data to CV JSON (creates enhanced version)."""
        enhanced_cv = self.cv.data.copy()
        
        # Add profile metrics
        if "profile_metrics" in self.metrics:
            enhanced_cv["metrics"] = self.metrics["profile_metrics"]
        
        # Add citation counts to publications
        for pub in enhanced_cv['publications']['conference_proceedings']:
            title = pub['title']
            if title in self.metrics["publications"]:
                pub['citations'] = self.metrics["publications"][title].get('citations', 0)
        
        for pub in enhanced_cv['publications']['book_chapters']:
            title = pub['title']
            if title in self.metrics["publications"]:
                pub['citations'] = self.metrics["publications"][title].get('citations', 0)
        
        # Save enhanced version
        with open('cv_data_with_metrics.json', 'w') as f:
            json.dump(enhanced_cv, f, indent=2)
        
        print("✓ Enhanced CV data saved to cv_data_with_metrics.json")


# Standalone usage
if __name__ == "__main__":
    cv = CVGenerator()
    metrics = PublicationMetrics(cv)
    
    print("=== Publication Metrics Fetcher ===\n")
    print("1. Fetch Google Scholar profile")
    print("2. Fetch all publication citations")
    print("3. Fetch ORCID metrics")
    print("4. Show metrics summary")
    print("5. Export metrics to JSON")
    print("6. Add metrics to CV data")
    print("7. Run full update (all above)")
    
    choice = input("\nSelect option (1-7): ").strip()
    
    if choice == "1":
        name = input("Author name (or press Enter for CV name): ").strip()
        metrics.fetch_google_scholar_profile(author_name=name if name else None)
    elif choice == "2":
        metrics.fetch_all_publication_metrics()
    elif choice == "3":
        orcid = input("ORCID ID (e.g., 0000-0002-7350-1987): ").strip()
        metrics.fetch_orcid_metrics(orcid)
    elif choice == "4":
        print(metrics.generate_metrics_summary())
    elif choice == "5":
        metrics.export_metrics_to_json()
    elif choice == "6":
        metrics.add_metrics_to_cv_data()
    elif choice == "7":
        print("\n🚀 Running full metrics update...\n")
        metrics.fetch_google_scholar_profile()
        time.sleep(2)
        metrics.fetch_orcid_metrics("0000-0002-7350-1987")
        time.sleep(2)
        metrics.fetch_all_publication_metrics()
        print(metrics.generate_metrics_summary())
        metrics.export_metrics_to_json()
        metrics.add_metrics_to_cv_data()
        print("\n✅ Full update complete!")
    else:
        print("Invalid option")